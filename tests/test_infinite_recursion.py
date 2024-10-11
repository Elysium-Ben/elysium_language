# tests/test_infinite_recursion.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

import textwrap

def test_infinite_recursion():
    code = textwrap.dedent("""
    def recurse():
        recurse()

    recurse()
    """)
    def recurse():
        recurse()

    recurse()
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter()
    # Assuming interpreter has a maximum recursion depth and raises RuntimeError
    with pytest.raises(RuntimeError) as exc_info:
        interpreter.execute(ast)
    assert "Maximum recursion depth exceeded" in str(exc_info.value)
