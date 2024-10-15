# tests/lexer/test_lexer_extended.py

import unittest
from src.lexer import Lexer, LexerError
from src.token import TokenType


class TestLexerExtended(unittest.TestCase):
    """Extended lexer tests."""

    def test_lexer_comments(self):
        code = """
        # This is a comment
        a = 5
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.IDENTIFIER,    # a
            TokenType.SPECIAL_CHAR,  # =
            TokenType.NUMBER,        # 5
            TokenType.EOF
        ]
        self.assertEqual([token.type for token in tokens], expected_types)

    def test_lexer_invalid_character(self):
        code = "a = 5 @"
        lexer = Lexer(code)
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        self.assertIn("Unknown character: @", str(context.exception))

    def test_lexer_multiple_newlines(self):
        code = "\n\n\n a = 5\n\n\n"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.IDENTIFIER,    # a
            TokenType.SPECIAL_CHAR,  # =
            TokenType.NUMBER,        # 5
            TokenType.EOF
        ]
        self.assertEqual([token.type for token in tokens], expected_types)

    def test_lexer_different_tokens(self):
        code = "def func(a, b): return a + b"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'def',       # Keyword
            'func',      # Identifier
            '(',         # Special character
            'a',         # Identifier
            ',',         # Special character
            'b',         # Identifier
            ')',         # Special character
            ':',         # Special character
            'return',    # Keyword
            'a',         # Identifier
            '+',         # Special character
            'b',         # Identifier
            None         # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_print_as_identifier(self):
        code = "print_var = 10"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.IDENTIFIER,    # print_var
            TokenType.SPECIAL_CHAR,  # =
            TokenType.NUMBER,        # 10
            TokenType.EOF
        ]
        self.assertEqual([token.type for token in tokens], expected_types)

    def test_lexer_print_keyword_as_identifier(self):
        code = "printable = True"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'printable',  # Identifier
            '=',          # Special character
            True,         # Boolean value
            None          # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_function_call(self):
        code = "func(a, b)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'func',      # Identifier
            '(',         # Special character
            'a',         # Identifier
            ',',         # Special character
            'b',         # Identifier
            ')',         # Special character
            None         # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_unknown_multichar_operator(self):
        code = "a == b"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'a',         # Identifier
            '==',        # Special character
            'b',         # Identifier
            None         # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_less_than_or_equal(self):
        code = "a <= b"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'a',         # Identifier
            '<=',        # Special character
            'b',         # Identifier
            None         # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_greater_than_or_equal(self):
        code = "a >= b"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'a',         # Identifier
            '>=',        # Special character
            'b',         # Identifier
            None         # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)


if __name__ == '__main__':
    unittest.main()
