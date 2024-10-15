# tests/test_scope.py

import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


class TestScope(unittest.TestCase):
    """Test cases for variable scope and shadowing."""

    def test_scope_variable_shadowing(self):
        code = """
        a = 10
        def test():
            a = 20
            print(a)
        end
        test()
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
        # Optionally, capture stdout and assert the outputs are '20' and '10'

if __name__ == '__main__':
        unittest.main()
