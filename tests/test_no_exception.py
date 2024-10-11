# tests/test_no_exception.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_no_exception(dedent_code, capfd):
    code = dedent_code("""
        x = 10
        y = x + 5
        print(y)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "15\n"
