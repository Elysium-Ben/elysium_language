# tests/test_infinite_loop.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter, InfiniteLoopError
from src.token import Token
from src.ast_node import ASTNode

def test_infinite_loop(dedent_code):
    code = dedent_code("""
        while True:
            pass
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    # Assuming Interpreter raises InfiniteLoopError after a certain number of iterations
    with pytest.raises(InfiniteLoopError):
        interpreter.execute()
