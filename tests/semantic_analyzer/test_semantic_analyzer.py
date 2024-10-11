# tests/semantic_analyzer/test_semantic_analyzer.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.token import Token
from src.ast_node import ASTNode

def test_semantic_analyzer_duplicate_variable(dedent_code):
    code = dedent_code("""
        x = 10
        x = 20  # Duplicate variable declaration
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()

def test_semantic_analyzer_undeclared_variable(dedent_code):
    code = dedent_code("""
        x = 10
        y = z + 5  # 'z' is undeclared
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()
