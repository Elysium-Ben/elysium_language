# tests/interpreter/test_exception_handling.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestInterpreterExceptionHandling(unittest.TestCase):
    """Interpreter tests for exception handling."""

    def test_interpreter_exception_propagation(self):
        code = """
        def func():
            raise Exception("Error")
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
        semantic_analyzer.visit(ast)
        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, capture stdout and assert the output is 'Exception caught'

if __name__ == '__main__':
    unittest.main()
