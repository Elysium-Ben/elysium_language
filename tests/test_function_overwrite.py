# tests/test_function_overwrite.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter


class TestFunctionOverwrite(unittest.TestCase):
    """Test cases for function overwriting."""

    def test_function_overwrite_success(self):
        code = """
        def func():
            print("First definition")
        end
        func()
        def func():
            print("Second definition")
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

        # Allow function overwriting in the semantic analyzer
        semantic_analyzer = SemanticAnalyzer(allow_function_overwrite=True)
        try:
            semantic_analyzer.visit(ast)
        except SemanticError as e:
            self.fail(f"SemanticError: {e}")

        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, capture stdout and assert the output

    def test_function_overwrite_not_allowed(self):
        code = """
        def func():
            print("First definition")
        end
        def func():
            print("Second definition")
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
        except ParserError as e:
            self.fail(f"ParserError: {e}")

        semantic_analyzer = SemanticAnalyzer(allow_function_overwrite=False)
        with self.assertRaises(SemanticError):
            semantic_analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
