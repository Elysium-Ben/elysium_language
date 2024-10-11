# tests/test_exception_handling.py

import textwrap
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

def test_exception_handling():
    code = textwrap.dedent("""
        x = 10
        y = x / 0  # This should raise a division by zero error
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter(ast)
    try:
        interpreter.execute()
    except ZeroDivisionError:
        pass
    else:
        assert False, "Expected ZeroDivisionError"
