# tests/semantic_analyzer/test_semantic_analyzer_extended.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError

class TestSemanticAnalyzerExtended(unittest.TestCase):
    """Extended semantic analyzer tests."""

    def test_semantic_analyzer_function_call_wrong_arguments(self):
        code = """
        def add(a, b):
            return a + b
        end
        result = add(2)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            semantic_analyzer.visit(ast)
        self.assertIn("Function 'add' expects 2 arguments but 1 was given", str(context.exception))

    def test_semantic_analyzer_undeclared_variable_complex(self):
        code = """
        def func():
            print(z)
        end
        func()
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            semantic_analyzer.visit(ast)
        self.assertIn("Undeclared variable: z", str(context.exception))
