# tests/test_function_overwrite.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.token import Token
from src.ast_node import ASTNode

def test_function_overwrite(dedent_code):
    code = dedent_code("""
        def func(a):
            return a + 1

        def func(a):
            return a + 2

        result = func(5)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()
