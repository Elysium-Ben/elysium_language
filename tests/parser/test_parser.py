# tests/parser/test_parser.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.ast_node import ASTNode


class TestParser(unittest.TestCase):
    """Parser tests for basic constructs."""

    def test_parser_basic_assignment(self):
        code = "a = 5"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        expected_ast = ASTNode('PROGRAM', children=[
            ASTNode('ASSIGN', value='a', children=[
                ASTNode('NUMBER', value=5)
            ])
        ])
        self.assertEqual(ast, expected_ast)

    def test_parser_print_statement(self):
        code = "print(10)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        expected_ast = ASTNode('PROGRAM', children=[
            ASTNode('PRINT', children=[
                ASTNode('NUMBER', value=10)
            ])
        ])
        self.assertEqual(ast, expected_ast)

if __name__ == '__main__':
    unittest.main()
