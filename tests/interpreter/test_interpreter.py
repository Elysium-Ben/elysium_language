# tests/interpreter/test_interpreter.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_interpreter_basic_assignment(dedent_code, capfd):
    code = dedent_code("""
        a = 5
        b = a + 3
        print(b)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "8\n"

def test_interpreter_multiple_assignments(dedent_code, capfd):
    code = dedent_code("""
        x = 10
        y = x * 2
        z = y - 5
        print(z)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "15\n"
