# tests/test_nested_functions.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_nested_functions():
    code = textwrap.dedent("""
    def outer():
        def inner():
            return 1
        return inner()

    x = outer()
    print(x)
    """)
    def outer():
        def inner():
            return 1
        return inner()

    x = outer()
    print(x)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify that 'outer' is in the symbol table with 'inner' defined within its scope
    assert 'outer' in analyzer.symbol_table
    outer_entry = analyzer.symbol_table['outer']
    assert 'inner' in outer_entry['body'].children[0].children  # Adjust based on implementation
    # Verify 'x' has type 'int'
    assert 'x' in analyzer.symbol_table
    assert analyzer.symbol_table['x'] == 'int'
