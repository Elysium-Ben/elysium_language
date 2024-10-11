# tests/interpreter/test_interpreter.py

import pytest
import textwrap
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

import textwrap

def test_interpreter_basic_execution(capfd):
    code = textwrap.dedent(textwrap.dedent("""
    x = 10
    y = x + 5
    print(y)
    """))
    x = 10
    y = x + 5
    print(y)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter(ast)  # Pass 'ast' here
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out.strip() == "15"
