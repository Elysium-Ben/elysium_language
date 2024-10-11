# tests/test_multiple_exceptions.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_multiple_exceptions():
    code = textwrap.dedent("""
    x = 10
    y = x / 0
    z = y + 5  # Multiple exceptions should be handled
    """)
    x = 10
    y = x / 0
    z = y + 5  # Multiple exceptions should be handled
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    # First exception occurs at y = x / 0
    with pytest.raises(ZeroDivisionError) as exc_info:
        analyzer.analyze(ast)
    assert "Division by zero" in str(exc_info.value)
