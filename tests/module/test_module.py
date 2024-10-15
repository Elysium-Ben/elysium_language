# tests/module/test_module.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter, InterpreterError

class TestModule(unittest.TestCase):
    """Test cases for module imports."""

    def test_module_import_success(self):
        code = """
        import math
        result = math.add(2, 3)
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
        try:
            semantic_analyzer.visit(ast)
        except SemanticError as e:
            self.fail(f"SemanticError: {e}")
        interpreter = Interpreter()
        try:
            interpreter.interpret(ast)
            # Optionally, capture stdout and assert the output is '5'
        except InterpreterError as e:
            self.fail(f"InterpreterError: {e}")

    def test_module_import_nonexistent(self):
        code = """
        import nonexistent_module
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
        except ParserError as e:
            self.fail(f"ParserError: {e}")
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            semantic_analyzer.visit(ast)
        self.assertIn("Module 'nonexistent_module' not found", str(context.exception))

    def test_module_function_not_found(self):
        code = """
        import math
        result = math.subtract(5, 3)
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
        with self.assertRaises(SemanticError) as context:
            semantic_analyzer.visit(ast)
        self.assertIn("Function 'subtract' not found in module 'math'", str(context.exception))
