# tests/test_basic_functionality.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter, InterpreterError


class TestBasicFunctionality(unittest.TestCase):
    """Test cases for basic functionality of the Elysium language."""

    def test_basic_arithmetic_operations(self):
        code = """
        a = 5 + 3 * 2
        print(a)
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
        # Optionally, capture stdout and assert the output is '11'

    def test_basic_variable_scope(self):
        code = """
        def test():
            a = 10
            print(a)
        end
        test()
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
        # Optionally, capture stdout and assert the output is '10'

if __name__ == '__main__':
    unittest.main()
