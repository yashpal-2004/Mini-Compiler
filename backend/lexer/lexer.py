from lexer.tokens import Token, TokenType

KEYWORDS = {
    "int": TokenType.KEYWORD,
    "float": TokenType.KEYWORD,
    "bool": TokenType.KEYWORD,
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "while": TokenType.KEYWORD,
    "return": TokenType.KEYWORD,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
}

class LexerError(Exception):
    def __init__(self, message, line, column, char):
        self.message = message
        self.line = line
        self.column = column
        self.char = char
        super().__init__(self.message)

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def advance(self):
        if self.pos < self.length:
            char = self.source[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None

    def peek(self):
        if self.pos < self.length:
            return self.source[self.pos]
        return None

    def skip_whitespace_and_comments(self):
        while self.peek() is not None:
            if self.peek().isspace():
                self.advance()
            elif self.peek() == '/' and self.pos + 1 < self.length and self.source[self.pos + 1] == '/':
                while self.peek() is not None and self.peek() != '\n':
                    self.advance()
            elif self.peek() == '#':
                while self.peek() is not None and self.peek() != '\n':
                    self.advance()
            else:
                break

    def get_next_token(self) -> Token:
        self.skip_whitespace_and_comments()

        if self.peek() is None:
            return Token(TokenType.EOF, "", self.line, self.column)

        start_column = self.column
        start_line = self.line
        char = self.advance()

        if char.isalpha() or char == '_':
            value = char
            while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
                value += self.advance()
            token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
            return Token(token_type, value, start_line, start_column)

        if char.isdigit():
            value = char
            is_float = False
            while self.peek() is not None and (self.peek().isdigit() or self.peek() == '.'):
                if self.peek() == '.':
                    if is_float:
                        break
                    is_float = True
                value += self.advance()
            return Token(TokenType.FLOAT if is_float else TokenType.INTEGER, value, start_line, start_column)

        if char == '+':
            return Token(TokenType.PLUS, char, start_line, start_column)
        if char == '-':
            return Token(TokenType.MINUS, char, start_line, start_column)
        if char == '*':
            return Token(TokenType.MULTIPLY, char, start_line, start_column)
        if char == '/':
            return Token(TokenType.DIVIDE, char, start_line, start_column)
        if char == '(':
            return Token(TokenType.LPAREN, char, start_line, start_column)
        if char == ')':
            return Token(TokenType.RPAREN, char, start_line, start_column)
        if char == '{':
            return Token(TokenType.LBRACE, char, start_line, start_column)
        if char == '}':
            return Token(TokenType.RBRACE, char, start_line, start_column)
        if char == ';':
            return Token(TokenType.SEMICOLON, char, start_line, start_column)
        
        if char == '=':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.EQUAL, "==", start_line, start_column)
            return Token(TokenType.ASSIGN, "=", start_line, start_column)
            
        if char == '<':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.LESS_EQUAL, "<=", start_line, start_column)
            return Token(TokenType.LESS, "<", start_line, start_column)

        if char == '>':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.GREATER_EQUAL, ">=", start_line, start_column)
            return Token(TokenType.GREATER, ">", start_line, start_column)
            
        if char == '!':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.NOT_EQUAL, "!=", start_line, start_column)
            raise LexerError(f"Unknown character '{char}'", start_line, start_column, char)
            
        if char == '&':
            if self.peek() == '&':
                self.advance()
                return Token(TokenType.AND, "&&", start_line, start_column)
            raise LexerError(f"Unknown character '{char}'", start_line, start_column, char)

        if char == '|':
            if self.peek() == '|':
                self.advance()
                return Token(TokenType.OR, "||", start_line, start_column)
            raise LexerError(f"Unknown character '{char}'", start_line, start_column, char)

        raise LexerError(f"Unknown character '{char}'", start_line, start_column, char)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
