# tests/semantic_analyzer/test_semantic_analyzer_function_call_with_wrong_arguments.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_function_call_with_missing_arguments():
    code = textwrap.dedent("""
    def add(a, b):
        return a + b

    result = add(5)  # Missing one argument
    """)
    def add(a, b):
        return a + b

    result = add(5)  # Missing one argument
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(TypeError) as exc_info:
        analyzer.analyze(ast)
    assert "Missing argument for 'add'" in str(exc_info.value)
