# tests/test_recursion.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_recursion_factorial(dedent_code, capfd):
    code = dedent_code("""
        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n - 1)

        result = factorial(5)
        print(result)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "120\n"
