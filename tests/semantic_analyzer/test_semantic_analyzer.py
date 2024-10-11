# tests/semantic_analyzer/test_semantic_analyzer.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

import textwrap

def test_semantic_analyzer_correct_code():
    code = textwrap.dedent("""
    x = 10
    print(x)
    """)
    x = 10
    print(x)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify that 'x' is in the symbol table and has type 'int'
    assert 'x' in analyzer.symbol_table
    assert analyzer.symbol_table['x'] == 'int'

def test_semantic_analyzer_undefined_variable():
    code = textwrap.dedent("""
    print(x)  # x is not defined
    """)
    print(x)  # x is not defined
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(NameError) as exc_info:
        analyzer.analyze(ast)
    assert "Undefined variable 'x'" in str(exc_info.value)

def test_semantic_analyzer_type_mismatch():
    code = textwrap.dedent("""
    x = 10
    y = "hello"
    z = x + y  # This should raise a type mismatch error
    """)
    x = 10
    y = "hello"
    z = x + y  # This should raise a type mismatch error
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(TypeError) as exc_info:
        analyzer.analyze(ast)
    assert "Type mismatch for '+' operator" in str(exc_info.value)

def test_semantic_analyzer_function_definition():
    code = textwrap.dedent("""
    def foo(a, b):
        return a + b

    result = foo(5, 10)
    print(result)
    """)
    def foo(a, b):
        return a + b

    result = foo(5, 10)
    print(result)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    # Verify that 'foo' is in the symbol table with correct parameters
    assert 'foo' in analyzer.symbol_table
    assert analyzer.symbol_table['foo']['params'] == ['a', 'b']
    # Further checks can be added to verify the function body

def test_semantic_analyzer_function_call_with_wrong_arguments():
    code = textwrap.dedent("""
    def foo(a):
        return a

    result = foo()  # Missing argument
    """)
    def foo(a):
        return a

    result = foo()  # Missing argument
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(TypeError) as exc_info:
        analyzer.analyze(ast)
    assert "Missing argument for 'foo'" in str(exc_info.value)
