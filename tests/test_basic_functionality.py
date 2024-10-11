import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.token import Token
from src.ast_node import ASTNode

def test_basic_assignment_and_print(dedent_code, capfd):
    code = dedent_code("""
        x = 10
        y = x + 5
        print(y)
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
                value=Token(token_type='IDENTIFIER', lexeme='x'),
                children=[
                    ASTNode(
                        node_type='INTEGER',
                        value=Token(token_type='INTEGER', lexeme='10')
                    )
                ]
            ),
            ASTNode(
                node_type='ASSIGN',
                value=Token(token_type='IDENTIFIER', lexeme='y'),
                children=[
                    ASTNode(
                        node_type='BIN_OP',
                        value=Token(token_type='PLUS', lexeme='+'),
                        children=[
                            ASTNode(
                                node_type='IDENTIFIER',
                                value=Token(token_type='IDENTIFIER', lexeme='x')
                            ),
                            ASTNode(
                                node_type='INTEGER',
                                value=Token(token_type='INTEGER', lexeme='5')
                            )
                        ]
                    )
                ]
            ),
            ASTNode(
                node_type='PRINT',
                children=[
                    ASTNode(
                        node_type='IDENTIFIER',
                        value=Token(token_type='IDENTIFIER', lexeme='y')
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast
