# tests/test_recursion.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestRecursion(unittest.TestCase):
    """Test cases for recursive function calls."""

    def test_recursion_factorial(self):
        code = """
        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n - 1)
            end
        end
        print(factorial(5))
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
        except ParserError as e:
            self.fail(f"ParserError: {e}")
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)
        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, capture stdout and assert the output is '120'

if __name__ == '__main__':
    unittest.main()
