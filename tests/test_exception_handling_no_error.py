# tests/test_exception_handling_no_error.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestExceptionHandlingNoError(unittest.TestCase):
    """Test cases where exceptions are not raised."""

    def test_exception_handling_no_error(self):
        code = """
        try:
            print("No exception")
        except Exception:
            print("This should not be printed")
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
        # Optionally, capture stdout and assert the output is 'No exception'

if __name__ == '__main__':
    unittest.main()
