# tests/test_exception_handling_wrong_exception.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_exception_handling_wrong_exception(dedent_code):
    code = dedent_code("""
        try:
            x = 10 / 0
        except ValueError:
            print("ValueError caught")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    with pytest.raises(ZeroDivisionError):
        interpreter.execute()
