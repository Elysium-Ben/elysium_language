# tests/test_exception_propagation.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter


class TestExceptionPropagation(unittest.TestCase):
    """Test cases for exception propagation in nested try-except blocks."""

    def test_exception_propagation_nested_try_except(self):
        code = """
        try:
            try:
                raise Exception
            except ValueError:
                print("Caught ValueError")
            end
        except Exception:
            print("Caught Exception")
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
        try:
            semantic_analyzer.visit(ast)
        except SemanticError as e:
            self.fail(f"SemanticError: {e}")

        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, capture stdout and assert the output is 'Caught Exception'

if __name__ == '__main__':
    unittest.main()
