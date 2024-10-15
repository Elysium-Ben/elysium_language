# tests/semantic_analyzer/test_semantic_analysis_function_definition.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError


class TestSemanticAnalysisFunctionDefinition(unittest.TestCase):
    """Semantic analyzer tests for function definitions."""

    def test_function_definition_success(self):
        code = """
        def add(a, b):
            return a + b
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        try:
            semantic_analyzer.visit(ast)
        except SemanticError as e:
            self.fail(f"SemanticError: {e}")

    def test_function_definition_duplicate(self):
        code = """
        def func():
            pass
        end
        def func():
            pass
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError):
            semantic_analyzer.visit(ast)

    def test_function_definition_missing_return(self):
        code = """
        def func():
            a = 10
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # Depending on language design, decide if missing return is an error
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
