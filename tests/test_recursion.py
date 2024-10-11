# tests/test_recursion.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

import textwrap

def test_recursion(capfd):
    code = textwrap.dedent("""
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)

    result = factorial(5)
    print(result)
    """)
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)

    result = factorial(5)
    print(result)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter()
    interpreter.execute(ast)
    captured = capfd.readouterr()
    assert captured.out.strip() == "120"
