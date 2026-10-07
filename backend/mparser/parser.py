from lexer.tokens import TokenType, Token
from mparser.ast import *

class ParserError(Exception):
    def __init__(self, message, line, column, suggestion):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        super().__init__(self.message)

class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type != TokenType.EOF]
        self.pos = 0
        self.length = len(self.tokens)

    def peek(self):
        if self.pos < self.length:
            return self.tokens[self.pos]
        return None

    def advance(self):
        if self.pos < self.length:
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    def match(self, token_type):
        token = self.peek()
        if token and token.type == token_type:
            return self.advance()
        return None

    def expect(self, token_type, expected_str=""):
        token = self.peek()
        if token and token.type == token_type:
            return self.advance()
        
        found = token.value if token else "EOF"
        line = token.line if token else (self.tokens[-1].line if self.tokens else 1)
        column = token.column if token else (self.tokens[-1].column if self.tokens else 1)
        
        expected = expected_str or token_type.value
        msg = f"Expected '{expected}', Found '{found}'"
        raise ParserError(msg, line, column, f"Check syntax near line {line}")

    def parse(self):
        declarations = []
        while self.peek():
            declarations.append(self.parse_function_declaration())
        return Program(declarations)

    def parse_function_declaration(self):
        type_token = self.peek()
        if type_token and type_token.value in ["int", "float", "bool"]:
            self.advance()
            return_type = type_token.value
        else:
            raise ParserError("Expected return type (int, float, bool)", 
                              type_token.line if type_token else 1, 
                              type_token.column if type_token else 1,
                              "Provide a valid return type for the function")

        name_token = self.expect(TokenType.IDENTIFIER, "function name")
        
        self.expect(TokenType.LPAREN, "(")
        self.expect(TokenType.RPAREN, ")")
        
        body = self.parse_block()
        return FunctionDeclaration(return_type, name_token.value, body)

    def parse_block(self):
        self.expect(TokenType.LBRACE, "{")
        statements = []
        while self.peek() and self.peek().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE, "}")
        return Block(statements)

    def parse_statement(self):
        token = self.peek()
        if token.value in ["int", "float", "bool"]:
            return self.parse_variable_declaration()
        elif token.type == TokenType.KEYWORD and token.value == "if":
            return self.parse_if_statement()
        elif token.type == TokenType.KEYWORD and token.value == "while":
            return self.parse_while_statement()
        elif token.type == TokenType.KEYWORD and token.value == "return":
            return self.parse_return_statement()
        else:
            return self.parse_assignment_or_expr_statement()

    def parse_variable_declaration(self):
        type_token = self.advance()
        name_token = self.expect(TokenType.IDENTIFIER, "variable name")
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()
            
        self.expect(TokenType.SEMICOLON, ";")
        return VariableDeclaration(type_token.value, name_token.value, initializer)

    def parse_if_statement(self):
        self.expect(TokenType.KEYWORD, "if")
        self.expect(TokenType.LPAREN, "(")
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN, ")")
        then_branch = self.parse_block()
        
        else_branch = None
        if self.peek() and self.peek().value == "else":
            self.advance()
            else_branch = self.parse_block()
            
        return IfStatement(condition, then_branch, else_branch)

    def parse_while_statement(self):
        self.expect(TokenType.KEYWORD, "while")
        self.expect(TokenType.LPAREN, "(")
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN, ")")
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_return_statement(self):
        self.expect(TokenType.KEYWORD, "return")
        value = None
        if not self.peek() or self.peek().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON, ";")
        return ReturnStatement(value)

    def parse_assignment_or_expr_statement(self):
        expr = self.parse_expression()
        
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, Identifier):
                token = self.peek()
                raise ParserError("Invalid assignment target", 
                                  token.line if token else 1, 
                                  token.column if token else 1,
                                  "Assign to a variable")
            value = self.parse_expression()
            self.expect(TokenType.SEMICOLON, ";")
            return Assignment(expr.name, value)
            
        self.expect(TokenType.SEMICOLON, ";")
        return expr

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.peek() and self.peek().type == TokenType.OR:
            op = self.advance()
            right = self.parse_logical_and()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.peek() and self.peek().type == TokenType.AND:
            op = self.advance()
            right = self.parse_equality()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.peek() and self.peek().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance()
            right = self.parse_comparison()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.peek() and self.peek().type in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op = self.advance()
            right = self.parse_term()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek() and self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.parse_factor()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_factor(self):
        left = self.parse_primary()
        while self.peek() and self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.advance()
            right = self.parse_primary()
            left = BinaryExpression(left, op.value, right)
        return left

    def parse_primary(self):
        token = self.advance()
        if not token:
            raise ParserError("Unexpected end of file", 1, 1, "Incomplete expression")
            
        if token.type == TokenType.INTEGER:
            return Literal(int(token.value), "int")
        elif token.type == TokenType.FLOAT:
            return Literal(float(token.value), "float")
        elif token.type == TokenType.BOOLEAN:
            return Literal(token.value == "true", "bool")
        elif token.type == TokenType.IDENTIFIER:
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, ")")
            return expr
            
        raise ParserError(f"Unexpected token '{token.value}'", token.line, token.column, "Check expression syntax")
