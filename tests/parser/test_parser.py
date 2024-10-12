# tests/parser/test_parser.py

import pytest
from src.lexer import Lexer  # Import the Lexer class
from src.parser import Parser  # Import the Parser class
from src.ast_node import ASTNode  # Import the ASTNode class
from src.token import Token  # Import the Token class

@pytest.fixture
def dedent_code():
    """Fixture to dedent multiline code strings."""
    import textwrap
    def _dedent_code(code):
        return textwrap.dedent(code).strip()
    return _dedent_code

def test_parser_basic_assignment(dedent_code):
    """Test parsing of a basic assignment statement."""
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
                        node_type='NUMBER',
                        value=5
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast

def test_parser_print_statement(dedent_code):
    """Test parsing of a print statement."""
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
                        node_type='NUMBER',
                        value=10
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast
