# tests/test_nested_try_except.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_nested_try_except():
    code = textwrap.dedent("""
    try:
        try:
            x = 10 / 0
        except ZeroDivisionError:
            print("Inner exception")
    except Exception:
        print("Outer exception")
    """)
    try:
        try:
            x = 10 / 0
        except ZeroDivisionError:
            print("Inner exception")
    except Exception:
        print("Outer exception")
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    # Assuming SemanticAnalyzer can handle nested try-except blocks
    analyzer.analyze(ast)
    # Since the inner exception is handled, no exception should propagate
    assert True  # If no exception, test passes
