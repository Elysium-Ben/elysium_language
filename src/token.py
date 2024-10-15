# src/token.py

from enum import Enum, auto

class TokenType(Enum):
    """Enumeration of possible token types."""
    IDENTIFIER = auto()
    NUMBER = auto()
    KEYWORD = auto()
    SPECIAL_CHAR = auto()
    STRING = auto()
    BOOLEAN = auto()
    EOF = auto()
    # Add more token types as needed

# Define keywords and special characters for easy reference
KEYWORDS = {
    'def', 'end', 'if', 'else', 'while', 'return', 'print', 'try', 'except', 'raise',
    'import', 'pass', 'and', 'or', 'not', 
}


SPECIAL_CHARACTERS = {
    '(', ')', '{', '}', '+', '-', '*', '/', '=', ';', ',', ':', '.', '==', '!=', '<', '>',
    '<=', '>=', '%'
}


class Token:
    """Token class representing the smallest units in the language."""

    def __init__(self, type_: TokenType, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
