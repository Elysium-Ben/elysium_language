# tests/interpreter/test_interpreter.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter, InterpreterError


class TestInterpreter(unittest.TestCase):
    """General interpreter tests."""

    def test_interpreter_basic_assignment_print(self):
        code = """
        a = 5
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
        semantic_analyzer.visit(ast)
        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, assert that '5' is printed

    def test_interpreter_string_assignment_print(self):
        code = """
        message = "Hello, World!"
        print(message)
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

    def test_interpreter_operator_precedence(self):
        code = """
        result = 2 + 3 * 4
        print(result)
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

    def test_interpreter_parenthesized_expression(self):
        code = """
        result = (2 + 3) * 4
        print(result)
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

    def test_interpreter_division_expression(self):
        code = """
        result = 10 / 2
        print(result)
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

    def test_interpreter_unhandled_exception(self):
        code = """
        raise Exception("Test exception")
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
