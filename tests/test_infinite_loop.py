# tests/test_infinite_loop.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

import textwrap

def test_infinite_loop():
    code = textwrap.dedent("""
    while True:
        pass
    """)
    while True:
        pass
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter()
    # Assuming interpreter has a mechanism to detect infinite loops and raise RuntimeError
    with pytest.raises(RuntimeError) as exc_info:
        interpreter.execute(ast)
    assert "Infinite loop detected" in str(exc_info.value)
