# tests/test_exception_handling_wrong_exception.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_exception_handling_wrong_exception():
    code = textwrap.dedent("""
    x = 10
    y = x / 0  # Should raise ZeroDivisionError
    """)
    x = 10
    y = x / 0  # Should raise ZeroDivisionError
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(ZeroDivisionError) as exc_info:
        analyzer.analyze(ast)
    assert "Division by zero" in str(exc_info.value)
