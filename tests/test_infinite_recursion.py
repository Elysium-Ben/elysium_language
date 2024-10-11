# tests/test_infinite_recursion.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter, InfiniteRecursionError
from src.token import Token
from src.ast_node import ASTNode

def test_infinite_recursion(dedent_code):
    code = dedent_code("""
        def recurse():
            recurse()

        recurse()
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    # Assuming Interpreter raises InfiniteRecursionError after reaching recursion limit
    with pytest.raises(InfiniteRecursionError):
        interpreter.execute()
