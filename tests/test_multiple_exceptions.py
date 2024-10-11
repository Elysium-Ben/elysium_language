# tests/test_multiple_exceptions.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_multiple_exceptions(dedent_code, capfd):
    code = dedent_code("""
        try:
            x = 10 / 0
        except ZeroDivisionError:
            print("ZeroDivisionError caught")
        except ValueError:
            print("ValueError caught")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "ZeroDivisionError caught\n"
