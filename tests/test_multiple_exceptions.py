# tests/test_multiple_exceptions.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestMultipleExceptions(unittest.TestCase):
    """Test cases for handling multiple exceptions."""

    def test_multiple_exceptions(self):
        code = """
        try:
            raise ValueError
        except TypeError:
            print("Caught TypeError")
        except ValueError:
            print("Caught ValueError")
        end
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
        # Optionally, capture stdout and assert the output is 'Caught ValueError'

if __name__ == '__main__':
    unittest.main()
