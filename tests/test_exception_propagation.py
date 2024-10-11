# tests/test_exception_propagation.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_exception_propagation_nested_try_except(dedent_code, capfd):
    code = dedent_code("""
        try:
            try:
                x = 10 / 0
            except ValueError:
                print("Inner ValueError")
        except ZeroDivisionError:
            print("Outer ZeroDivisionError")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "Outer ZeroDivisionError\n"
