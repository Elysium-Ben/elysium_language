# tests/lexer/test_lexer_strings.py

import unittest
from src.lexer import Lexer, LexerError
from src.token import TokenType


class TestLexerStrings(unittest.TestCase):
    """Lexer tests for string handling."""

    def test_lexer_strings_simple(self):
        code = 'message = "Hello, World!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'message',    # Identifier
            '=',          # Special character
            'Hello, World!',  # String
            None          # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_strings_with_escape_characters(self):
        code = r'message = "Line1\nLine2"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'message',       # Identifier
            '=',             # Special character
            'Line1\nLine2',  # String with newline escape
            None             # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_strings_empty(self):
        code = 'empty_string = ""'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'empty_string',  # Identifier
            '=',             # Special character
            '',              # Empty string
            None             # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_strings_with_escaped_quote(self):
        code = r'message = "He said, \"Hello\""'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'message',            # Identifier
            '=',                  # Special character
            'He said, "Hello"',   # String with escaped quotes
            None                  # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_strings_unterminated(self):
        code = 'message = "Hello, World!'
        lexer = Lexer(code)
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        self.assertIn("Unterminated string literal", str(context.exception))

    def test_lexer_strings_with_invalid_escape(self):
        code = r'message = "Hello,\x World!"'
        lexer = Lexer(code)
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        self.assertIn("Invalid escape character", str(context.exception))

    def test_lexer_strings_with_tab_escape(self):
        code = r'message = "Hello,\tWorld!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'message',      # Identifier
            '=',            # Special character
            'Hello,\tWorld!',  # String with tab escape
            None            # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)

    def test_lexer_strings_with_backslash_escape(self):
        code = r'message = "Path\\to\\file"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_values = [
            'message',         # Identifier
            '=',               # Special character
            'Path\\to\\file',  # String with backslashes
            None               # EOF
        ]
        self.assertEqual([token.value for token in tokens], expected_values)


if __name__ == '__main__':
    unittest.main()
