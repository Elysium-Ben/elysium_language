# tests/semantic_analyzer/test_semantic_analyzer.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError


class TestSemanticAnalyzer(unittest.TestCase):
    """Semantic analyzer tests for variable usage."""

    def test_semantic_analyzer_duplicate_variable(self):
        code = """
        a = 5
        a = 10
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # Assuming variable redeclaration is allowed
        semantic_analyzer = SemanticAnalyzer()
        try:
            semantic_analyzer.visit(ast)
        except SemanticError as e:
            self.fail(f"SemanticError: {e}")

if __name__ == '__main__':
    unittest.main()
