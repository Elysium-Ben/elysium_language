import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.token import Token
from src.ast_node import ASTNode

def test_exception_handling_try_except(dedent_code, capfd):
    code = dedent_code("""
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    expected_ast = ASTNode(
        node_type='TRY',
        children=[
            ASTNode(
                node_type='EXCEPTION',
                children=[
                    ASTNode(
                        node_type='ASSIGN',
                        value=Token(token_type='IDENTIFIER', lexeme='x'),
                        children=[
                            ASTNode(
                                node_type='BIN_OP',
                                value=Token(token_type='DIV', lexeme='/'),
                                children=[
                                    ASTNode(
                                        node_type='INTEGER',
                                        value=Token(token_type='INTEGER', lexeme='1')
                                    ),
                                    ASTNode(
                                        node_type='INTEGER',
                                        value=Token(token_type='INTEGER', lexeme='0')
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            ASTNode(
                node_type='EXCEPT',
                value=Token(token_type='IDENTIFIER', lexeme='ZeroDivisionError'),
                children=[
                    ASTNode(
                        node_type='PRINT',
                        children=[
                            ASTNode(
                                node_type='STRING',
                                value=Token(token_type='STRING', lexeme='"Cannot divide by zero"')
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast
