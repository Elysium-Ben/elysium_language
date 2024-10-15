# tests/test_infinite_recursion.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter, InterpreterError


class TestInfiniteRecursion(unittest.TestCase):
    """Test cases for infinite recursion detection."""

    def test_infinite_recursion(self):
        code = """
        def recurse():
            recurse()
        end
        recurse()
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
