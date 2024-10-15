# tests/parser/test_parser_extended.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.ast_node import ASTNode


class TestParserExtended(unittest.TestCase):
    """Extended parser tests."""

    def test_parser_multiple_assignments(self):
        code = """
        a = 5
        b = a + 3
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # Build expected AST accordingly

    def test_parser_parenthesized_expression(self):
        code = "result = (2 + 3) * 4"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # Build expected AST accordingly

    def test_parser_syntax_error_unexpected_token(self):
        code = "print 10"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(ParserError):
            parser.parse()

    def test_parser_division_expression(self):
        code = "result = 10 / 2"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # Build expected AST accordingly

if __name__ == '__main__':
    unittest.main()
