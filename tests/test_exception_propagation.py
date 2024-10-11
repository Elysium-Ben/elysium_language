# tests/test_exception_propogation.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_exception_propagation():
    code = textwrap.dedent("""
    def divide(a, b):
        return a / b

    result = divide(10, 0)  # Should propagate ZeroDivisionError
    """)
    def divide(a, b):
        return a / b

    result = divide(10, 0)  # Should propagate ZeroDivisionError
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(ZeroDivisionError) as exc_info:
        analyzer.analyze(ast)
    assert "Division by zero" in str(exc_info.value)
