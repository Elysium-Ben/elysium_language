# tests/semantic_analyzer/test_try_except.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError

class TestTryExcept(unittest.TestCase):
    """Test cases for try-except blocks in the semantic analyzer."""

    def test_try_except_successful_handling(self):
        code = """
        try:
            a = 5 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
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

    def test_try_except_handling_specific_exception(self):
        code = """
        try:
            a = int("abc")
        except ValueError:
            print("Invalid integer")
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
