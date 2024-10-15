# tests/test_exception_handling.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter, InterpreterError


class TestExceptionHandling(unittest.TestCase):
    """Test cases for exception handling."""

    def test_exception_propagation(self):
        code = """
        def func():
            raise Exception
        end
        try:
            func()
        except Exception:
            print("Exception caught")
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
        # Optionally, capture stdout and assert the output is 'Exception caught'

if __name__ == '__main__':
    unittest.main()
