# tests/test_nested_exception_handling.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestNestedExceptionHandling(unittest.TestCase):
    """Test cases for nested exception handling."""

    def test_nested_exception_handling(self):
        code = """
        try:
            try:
                raise ValueError
            except TypeError:
                print("Caught TypeError")
            end
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
