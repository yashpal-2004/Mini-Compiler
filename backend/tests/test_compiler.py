from lexer.lexer import Lexer
from mparser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from tac.generator import TACGenerator
from optimizer.optimizer import Optimizer
from codegen.generator import CodeGenerator

def test_lexer_basic():
    source = "int x = 10;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert len(tokens) == 6 # int, x, =, 10, ;, EOF
    assert tokens[0].type.name == "KEYWORD"
    assert tokens[1].type.name == "IDENTIFIER"
    assert tokens[3].type.name == "INTEGER"

def test_parser_basic():
    source = "int main() { int x = 10; return x; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast.type == "Program"
    assert len(ast.declarations) == 1
    assert ast.declarations[0].type == "FunctionDeclaration"
    assert ast.declarations[0].name == "main"

def test_semantic_analyzer():
    source = "int main() { int x = 10; return x; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    assert "main" in analyzer.symbol_table.symbols
    assert "x" in analyzer.symbol_table.symbols

def test_tac_generator():
    source = "int main() { int x = 10; return x; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    tac_gen = TACGenerator(ast)
    tac = tac_gen.generate()
    assert len(tac) > 0

def test_optimizer():
    # Constant folding case
    source = "int main() { int x = 2 * 3; return x; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    tac_gen = TACGenerator(ast)
    tac = tac_gen.generate()
    
    optimizer = Optimizer(tac)
    opt_tac, _ = optimizer.optimize()
    # Check if 6 is in the optimized tac
    assert any("6" in t.formatted for t in opt_tac)

def test_codegen():
    source = "int main() { int x = 10; return x; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    tac_gen = TACGenerator(ast)
    tac = tac_gen.generate()
    codegen = CodeGenerator(tac)
    assembly = codegen.generate()
    assert len(assembly) > 0
    assert "RET x" in assembly or "RET" in "\n".join(assembly)

def test_full_pipeline():
    # End-to-end integration test
    source = """
    int main() {
        int a = 10;
        int b = 20;
        int c = a + b * 2;
        if (c > 30) {
            c = c + 5;
        }
        return c;
    }
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    tac_gen = TACGenerator(ast)
    tac = tac_gen.generate()
    optimizer = Optimizer(tac)
    opt_tac, _ = optimizer.optimize()
    codegen = CodeGenerator(opt_tac)
    assembly = codegen.generate()
    
    assert len(tokens) > 0
    assert ast is not None
    assert len(analyzer.symbol_table.symbols) > 0
    assert len(tac) > 0
    assert len(opt_tac) > 0
    assert len(assembly) > 0
