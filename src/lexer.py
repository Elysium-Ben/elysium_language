# src/lexer.py

from src.token import Token  # Import the Token class

class LexerError(Exception):
    """Custom exception for lexer errors."""
    pass

class Lexer:
    def __init__(self, text):
        """
        Initialize the Lexer.
        
        :param text: The input code as a string.
        """
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def advance(self):
        """Advance to the next character in the input."""
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def peek(self):
        """Peek at the next character without advancing."""
        next_pos = self.position + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        return None

    def skip_comment(self):
        """Skip over comments starting with '#'."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def tokenize_number(self):
        """Tokenize a numerical value."""
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(token_type='NUMBER', value=int(num_str))

    def tokenize_identifier(self):
        """Tokenize identifiers and keywords."""
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str == 'print':
            return Token(token_type='PRINT', value=id_str)
        return Token(token_type='IDENTIFIER', value=id_str)

    def tokenize(self):
        """
        Convert the input code into a list of tokens.
        
        :return: A list of Token objects.
        """
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':
                    # Avoid adding multiple consecutive NEWLINE tokens
                    if tokens and tokens[-1].token_type != 'NEWLINE':
                        tokens.append(Token(token_type='NEWLINE', value='\n'))
                self.advance()
            elif self.current_char == '#':  # Handle comments
                self.skip_comment()
            elif self.current_char.isdigit():
                tokens.append(self.tokenize_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.tokenize_identifier())
            elif self.current_char == '=':
                tokens.append(Token(token_type='ASSIGN', value='='))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(token_type='PLUS', value='+'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(token_type='LPAREN', value='('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(token_type='RPAREN', value=')'))
                self.advance()
            elif self.current_char == '/':
                if self.peek() == '/':
                    self.skip_comment()
                else:
                    tokens.append(Token(token_type='DIVIDE', value='/'))
                    self.advance()
            else:
                raise LexerError(f"Unexpected character: {self.current_char}")
        
        # Remove trailing NEWLINE if present to prevent an extra NEWLINE before EOF
        if tokens and tokens[-1].token_type == 'NEWLINE':
            tokens.pop()
        
        # Append EOF token to signify the end of input
        tokens.append(Token(token_type='EOF', value=None))
    
        return tokens
