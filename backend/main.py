from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import CompileRequest, CompileResponse
from lexer.lexer import Lexer, LexerError
from mparser.parser import Parser, ParserError
from semantic.analyzer import SemanticAnalyzer, SemanticError
from tac.generator import TACGenerator
from optimizer.optimizer import Optimizer
from codegen.generator import CodeGenerator
from interpreter.interpreter import Interpreter

app = FastAPI(title="Mini Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/compile", response_model=CompileResponse)
def compile_code(request: CompileRequest):
    response = CompileResponse(success=True)
    
    try:
        # 1. Lexical Analysis
        lexer = Lexer(request.sourceCode)
        tokens = lexer.tokenize()
        response.tokens = [t.to_dict() for t in tokens]
        
        if not tokens or (len(tokens) == 1 and tokens[0].type.name == "EOF"):
            return response
            
        # 2. Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        response.ast = ast.to_dict()
        
        # 3. Semantic Analysis
        analyzer = SemanticAnalyzer(ast)
        analyzer.analyze()
        response.symbolTable = [s.to_dict() for s in analyzer.symbol_table.symbols.values()]
        
        # 3.5 Interpreter Analysis
        interpreter = Interpreter(ast)
        analysis_warnings = interpreter.run()
        
        response.semanticWarnings = analyzer.warnings + analysis_warnings
        response.semanticErrors = analyzer.semantic_errors
        
        # 4. TAC Generation
        tac_gen = TACGenerator(ast)
        tac = tac_gen.generate()
        response.tac = [t.to_dict() for t in tac]
        
        # 5. Optimization
        optimizer = Optimizer(tac)
        optimized_tac, optimizations = optimizer.optimize()
        response.optimizedTac = [t.to_dict() for t in optimized_tac]
        response.optimizations = optimizations
        
        # 6. Code Generation
        codegen = CodeGenerator(optimized_tac)
        assembly = codegen.generate()
        response.assembly = assembly

    except LexerError as e:
        response.success = False
        response.phase = "lexical"
        response.errors.append({
            "phase": "lexical",
            "type": "LEXICAL ERROR",
            "message": e.message,
            "line": e.line,
            "column": e.column,
            "suggestion": f"Remove '{e.char}' or use a supported operator."
        })
    except ParserError as e:
        response.success = False
        response.phase = "syntax"
        response.errors.append({
            "phase": "syntax",
            "type": "SYNTAX ERROR",
            "message": e.message,
            "line": e.line,
            "column": e.column,
            "suggestion": e.suggestion
        })
    except SemanticError as e:
        response.success = False
        response.phase = "semantic"
        response.errors.append({
            "phase": "semantic",
            "type": "SEMANTIC ERROR",
            "message": e.message,
            "line": e.line,
            "column": e.column,
            "suggestion": e.suggestion
        })
    except Exception as e:
        response.success = False
        response.phase = "unknown"
        response.errors.append({
            "phase": "unknown",
            "type": "INTERNAL ERROR",
            "message": str(e),
            "line": 0,
            "column": 0,
            "suggestion": "Check server logs"
        })
        
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
