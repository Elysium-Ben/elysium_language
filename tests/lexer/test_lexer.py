# tests/lexer/test_lexer.py

import unittest
from src.lexer import Lexer, LexerError
from src.token import TokenType


class TestLexer(unittest.TestCase):
    """Basic lexer tests."""

    def test_basic_tokens(self):
        code = "a = 5"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.IDENTIFIER,   # a
            TokenType.SPECIAL_CHAR, # =
            TokenType.NUMBER,       # 5
            TokenType.EOF
        ]
        self.assertEqual([token.type for token in tokens], expected_types)

if __name__ == '__main__':
    unittest.main()
