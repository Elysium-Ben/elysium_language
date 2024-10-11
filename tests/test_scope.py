# tests/test_scope.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_scope():
    code = textwrap.dedent("""
    x = 10
    def foo():
        y = x + 5
        return y
    """)
    x = 10
    def foo():
        y = x + 5
        return y
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify that 'x' is defined globally and 'y' is defined within 'foo'
    assert 'x' in analyzer.symbol_table
    assert analyzer.symbol_table['x'] == 'int'
    assert 'foo' in analyzer.symbol_table
    foo_entry = analyzer.symbol_table['foo']
    assert foo_entry['params'] == []
    # Depending on your SemanticAnalyzer's implementation, verify 'y' is within 'foo's scope
    # Example (adjust based on your actual symbol table structure):
    assert 'y' in foo_entry['body'].children[0].children[0].children[0].value
