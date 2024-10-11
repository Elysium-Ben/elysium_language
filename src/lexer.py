# src/lexer.py

import re

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = {
            "print": "PRINT",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "def": "DEF",
            "return": "RETURN",
            "try": "TRY",
            "except": "EXCEPT",
            "raise": "RAISE",
            "import": "IMPORT",
        }

    def tokenize(self):
        code = self.code
        code = code.strip()
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Simple regex-based tokenization
            tokens_in_line = re.findall(r'\b\w+\b|[=+*/()-]', line)
            for tok in tokens_in_line:
                if tok in self.keywords:
                    self.tokens.append(Token(self.keywords[tok]))
                elif tok.isdigit():
                    self.tokens.append(Token("INTEGER", int(tok)))
                elif tok.isidentifier():
                    self.tokens.append(Token("IDENTIFIER", tok))
                elif tok == "=":
                    self.tokens.append(Token("ASSIGN"))
                elif tok == "+":
                    self.tokens.append(Token("PLUS"))
                elif tok == "-":
                    self.tokens.append(Token("MINUS"))
                elif tok == "*":
                    self.tokens.append(Token("MULTIPLY"))
                elif tok == "/":
                    self.tokens.append(Token("DIVIDE"))
                elif tok == "(":
                    self.tokens.append(Token("LPAREN"))
                elif tok == ")":
                    self.tokens.append(Token("RPAREN"))
                else:
                    raise SyntaxError(f"Unknown token: {tok}")
        self.tokens.append(Token("EOF"))
        return self.tokens
