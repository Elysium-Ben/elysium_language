# tests/test_nested_functions.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_nested_functions(dedent_code, capfd):
    code = dedent_code("""
        def outer(a):
            def inner(b):
                return a + b
            return inner(5)

        result = outer(10)
        print(result)
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
    assert captured.out == "15\n"
