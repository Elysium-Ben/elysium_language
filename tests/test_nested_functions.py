# tests/test_nested_functions.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestNestedFunctions(unittest.TestCase):
    """Test cases for nested function definitions."""

    def test_nested_functions(self):
        code = """
        def outer():
            def inner():
                print("Inner function")
            end
            inner()
        end
        outer()
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
        # Optionally, capture stdout and assert the output is 'Inner function'

if __name__ == '__main__':
    unittest.main()
