import re
from src.token import Token

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position] if self.code else None

    def advance(self):
        """Move the position one character forward."""
        self.position += 1
        self.current_char = self.code[self.position] if self.position < len(self.code) else None

    def tokenize(self):
        """Convert input code into a list of tokens."""
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':
                    if tokens and tokens[-1].token_type != 'NEWLINE':  # Avoid multiple consecutive newlines
                        tokens.append(Token(token_type='NEWLINE', value='\n'))  # Changed 'type' to 'token_type'
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.tokenize_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.tokenize_identifier())
            elif self.current_char == '=':
                tokens.append(Token(token_type='ASSIGN', value='='))  # Changed 'type' to 'token_type'
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(token_type='PLUS', value='+'))  # Changed 'type' to 'token_type'
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(token_type='LPAREN', value='('))  # Changed 'type' to 'token_type'
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(token_type='RPAREN', value=')'))  # Changed 'type' to 'token_type'
                self.advance()
            elif self.current_char == '/':
                if self.peek() == '/':
                    self.skip_comment()
                else:
                    tokens.append(Token(token_type='DIVIDE', value='/'))  # Changed 'type' to 'token_type'
                    self.advance()
            else:
                raise LexerError(f"Unexpected character: {self.current_char}")
        
        # Ensure no trailing NEWLINE before EOF
        if tokens and tokens[-1].token_type == 'NEWLINE':
            tokens.pop()

        tokens.append(Token(token_type='EOF', value=None))  # Changed 'type' to 'token_type'
        return tokens

    def tokenize_number(self):
        """Tokenize a number."""
        number_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            number_str += self.current_char
            self.advance()
        return Token(token_type='NUMBER', value=int(number_str))  # Changed 'type' to 'token_type'

    def tokenize_identifier(self):
        """Tokenize an identifier or keyword."""
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()

        if id_str == 'print':
            return Token(token_type='PRINT', value='print')  # Changed 'type' to 'token_type'
        return Token(token_type='IDENTIFIER', value=id_str)  # Changed 'type' to 'token_type'

    def skip_comment(self):
        """Skip a comment."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def peek(self):
        """Look at the next character without advancing the position."""
        peek_pos = self.position + 1
        return self.code[peek_pos] if peek_pos < len(self.code) else None
