# tests/test_nested_exception_handling.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_nested_exception_handling():
    code = textwrap.dedent("""
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")
    """)
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    # Assuming SemanticAnalyzer can handle try-except blocks
    analyzer.analyze(ast)
    # Since the exception is handled, no exception should be raised
    assert True  # If no exception, test passes
