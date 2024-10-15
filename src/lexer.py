# src/lexer.py

from src.token import Token, TokenType, KEYWORDS, SPECIAL_CHARACTERS

class LexerError(Exception):
    """Custom exception for lexer errors."""
    pass

class Lexer:
    """Lexer class for tokenizing input text."""

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def advance(self):
        """Advance the 'position' and set 'current_char'."""
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def peek(self):
        """Look ahead at the next character without consuming it."""
        peek_pos = self.position + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return ''  # Return empty string instead of None

    def tokenize(self):
        """Tokenize the entire input text."""
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()    
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self._identifier())
            elif self.current_char.isdigit():
                tokens.append(self._number())
            elif self.current_char == '"':
                tokens.append(self._string())
            elif self.current_char in SPECIAL_CHARACTERS:
                tokens.append(self._special_character())
            else:
                raise LexerError(f"Unknown character: {self.current_char}")
        tokens.append(Token(TokenType.EOF, None))
        return tokens

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        # Do not advance here; let the main loop handle the newline
        
    def _identifier(self):
        """Handle identifiers and keywords."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result in ('True', 'False'):
            return Token(TokenType.BOOLEAN, result == 'True')
        token_type = TokenType.KEYWORD if result in KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, result)

    def _number(self):
        """Handle numbers."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result))

    def _string(self):
        """Handle string literals."""
        self.advance()  # Skip the opening quote
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char in ['"', '\\', 'n', 't']:
                    escape_sequences = {'n': '\n', 't': '\t'}
                    result += escape_sequences.get(self.current_char, self.current_char)
                else:
                    raise LexerError(f"Invalid escape character: {self.current_char}")
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise LexerError("Unterminated string literal")
        self.advance()  # Skip the closing quote
        return Token(TokenType.STRING, result)

    def _special_character(self):
        char = self.current_char
        next_char = self.peek()
        if char + next_char in ('==', '!=', '>=', '<='):
            char += next_char
            self.advance()
            self.advance()
            return Token(TokenType.SPECIAL_CHAR, char)
        else:
            self.advance()
            return Token(TokenType.SPECIAL_CHAR, char)

