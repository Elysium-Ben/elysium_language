# tests/parser/test_parser.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_node import ASTNode

import textwrap

def test_parser_simple_assignment():
    code = textwrap.dedent("""
    x = 10
    """)
    x = 10
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = ASTNode(
        type='Program',
        children=[
            ASTNode(
                type='Assignment',
                value='x',
                children=[
                    ASTNode(type='Literal', value=10, children=[])
                ]
            )
        ]
    )
    assert ast == expected_ast

def test_parser_print_statement():
    code = textwrap.dedent("""
    print(10)
    """)
    print(10)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = ASTNode(
        type='Program',
        children=[
            ASTNode(
                type='Print',
                children=[
                    ASTNode(type='Literal', value=10, children=[])
                ]
            )
        ]
    )
    assert ast == expected_ast

def test_parser_function_definition():
    code = textwrap.dedent("""
    def foo():
        return 10
    """)
    def foo():
        return 10
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = ASTNode(
        type='Program',
        children=[
            ASTNode(
                type='FunctionDef',
                value='foo',
                children=[
                    ASTNode(type='Parameters', children=[]),
                    ASTNode(
                        type='Block',
                        children=[
                            ASTNode(
                                type='Return',
                                children=[
                                    ASTNode(type='Literal', value=10, children=[])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast
