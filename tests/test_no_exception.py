# tests/test_no_exception.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestNoException(unittest.TestCase):
    """Test cases where no exceptions occur."""

    def test_no_exception(self):
        code = """
        print("No exceptions here")
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
        # Optionally, capture stdout and assert the output is 'No exceptions here'

if __name__ == '__main__':
    unittest.main()
