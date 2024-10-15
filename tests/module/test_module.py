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
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)
        interpreter = Interpreter()
        interpreter.interpret(ast)
        # Optionally, capture stdout and assert the output is '5'

    def test_module_import_nonexistent(self):
        code = """
        import nonexistent
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(SemanticError):
            ast = parser.parse()
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.visit(ast)

    def test_module_function_not_found(self):
        code = """
        import math
        result = math.subtract(5, 2)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError):
            semantic_analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
