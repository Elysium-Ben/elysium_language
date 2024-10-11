# tests/test_scope.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_scope_variable_shadowing(dedent_code, capfd):
    code = dedent_code("""
        x = 10
        def func():
            x = 5
            print(x)
        func()
        print(x)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out == "5\n10\n"
