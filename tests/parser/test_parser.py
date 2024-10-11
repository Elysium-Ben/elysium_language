# tests/parser/test_parser.py

from src.lexer import Lexer  # Import the Lexer
from src.parser import Parser
from src.ast_node import ASTNode

def test_parser_basic_assignment(dedent_code):
    code = dedent_code("""
        a = 5
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    expected_ast = ASTNode(
        node_type='PROGRAM',
        children=[
            ASTNode(
                node_type='ASSIGN',
                value='a',
                children=[
                    ASTNode(
                        node_type='NUMBER',  # Updated from 'INTEGER' to 'NUMBER'
                        value=5
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast


def test_parser_print_statement(dedent_code):
    code = dedent_code("""
        print(10)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    expected_ast = ASTNode(
        node_type='PROGRAM',
        children=[
            ASTNode(
                node_type='PRINT',
                children=[
                    ASTNode(
                        node_type='NUMBER',  # Updated from 'INTEGER' to 'NUMBER'
                        value=10
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast
