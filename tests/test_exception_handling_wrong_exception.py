# tests/test_exception_handling_wrong_exception.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter, InterpreterError


class TestExceptionHandlingWrongException(unittest.TestCase):
    """Test cases where the wrong exception is handled."""

    def test_exception_handling_wrong_exception(self):
        code = """
        try:
            raise ValueError("An error occurred")
        except TypeError:
            print("Caught TypeError")
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)
        interpreter = Interpreter()
        with self.assertRaises(InterpreterError):
            interpreter.interpret(ast)

if __name__ == '__main__':
    unittest.main()
