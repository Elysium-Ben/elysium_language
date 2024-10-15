# tests/test_unhandled_exception.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter, InterpreterError


class TestUnhandledException(unittest.TestCase):
    """Test cases for unhandled exceptions."""

    def test_unhandled_exception(self):
        code = """
        raise Exception("Unhandled exception")
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
