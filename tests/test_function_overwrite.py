# tests/test_function_overwrite.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_function_overwrite():
    code = textwrap.dedent("""
    def foo():
        return 1

    def foo():
        return 2

    x = foo()
    print(x)
    """)
    def foo():
        return 1

    def foo():
        return 2

    x = foo()
    print(x)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify that 'foo' is in the symbol table and refers to the second definition
    assert 'foo' in analyzer.symbol_table
    foo_entry = analyzer.symbol_table['foo']
    assert foo_entry['params'] == []
    # Assuming 'foo' returns an integer
    assert 'x' in analyzer.symbol_table
    assert analyzer.symbol_table['x'] == 'int'
