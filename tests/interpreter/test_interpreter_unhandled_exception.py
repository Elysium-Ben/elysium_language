# tests/interpreter/test_interpreter_unhandled_exception.py

import pytest
import textwrap
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

import textwrap

def test_interpreter_unhandled_exception():
    code = textwrap.dedent(textwrap.dedent("""
    def divide(a, b):
        return a / b

    result = divide(10, 0)  # Unhandled exception: division by zero
    """))
    def divide(a, b):
        return a / b

    result = divide(10, 0)  # Unhandled exception: division by zero
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter()
    with pytest.raises(ZeroDivisionError) as exc_info:
        interpreter.execute(ast)
    assert "Division by zero" in str(exc_info.value)
