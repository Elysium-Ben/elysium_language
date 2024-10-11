# tests/test_unhandled_exception.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_unhandled_exception(dedent_code):
    code = dedent_code("""
        x = 10 / 0
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    with pytest.raises(ZeroDivisionError):
        interpreter.execute()
