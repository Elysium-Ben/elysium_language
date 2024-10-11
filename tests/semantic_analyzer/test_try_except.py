# tests/semantic_analyzer/test_try_except.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.token import Token
from src.ast_node import ASTNode

def test_try_except_correct(dedent_code):
    code = dedent_code("""
        try:
            x = 10 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    # Assuming no exception means pass

def test_try_except_wrong_exception(dedent_code):
    code = dedent_code("""
        try:
            x = 10 / 0
        except ValueError:
            print("Cannot divide by zero")
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()
