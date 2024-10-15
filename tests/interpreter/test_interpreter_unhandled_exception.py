# tests/interpreter/test_interpreter_unhandled_exception.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter, InterpreterError


class TestInterpreterUnhandledException(unittest.TestCase):
    """Interpreter tests for unhandled exceptions."""

    def test_interpreter_unhandled_exception(self):
        code = """
        def func():
            raise Exception("Unhandled")
        end
        func()
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
        with self.assertRaises(InterpreterError):
            interpreter.interpret(ast)

if __name__ == '__main__':
    unittest.main()
