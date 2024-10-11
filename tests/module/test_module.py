# tests/module/test_module.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter
from src.token import Token
from src.ast_node import ASTNode

def test_module_functionality(dedent_code, capfd):
    code = dedent_code("""
        def greet(name):
            print("Hello, " + name + "!")

        greet("Elysium")
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
    assert captured.out == "Hello, Elysium!\n"
