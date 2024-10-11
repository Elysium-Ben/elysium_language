# tests/test_no_exception.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_no_exception():
    code = textwrap.dedent("""
    a = 5
    b = a + 10
    """)
    a = 5
    b = a + 10
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify 'a' and 'b' are in the symbol table with type 'int'
    assert 'a' in analyzer.symbol_table
    assert analyzer.symbol_table['a'] == 'int'
    assert 'b' in analyzer.symbol_table
    assert analyzer.symbol_table['b'] == 'int'
