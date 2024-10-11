# tests/test_exception_handling_no_error.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_exception_handling_no_error(dedent_code, capfd):
    code = dedent_code("""
        try:
            x = 10 / 2
        except ZeroDivisionError:
            print("Cannot divide by zero")
        print(x)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "5.0\n"
