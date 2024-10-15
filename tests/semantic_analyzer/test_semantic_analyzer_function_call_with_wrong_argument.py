# tests/semantic_analyzer/test_semantic_analyzer_function_call_with_wrong_argument.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError


class TestFunctionCallWrongArgument(unittest.TestCase):
    """Test cases for function calls with wrong arguments."""

    def test_function_call_wrong_number_of_arguments(self):
        code = """
        def add(a, b):
            return a + b
        end
        result = add(1)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError):
            semantic_analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
