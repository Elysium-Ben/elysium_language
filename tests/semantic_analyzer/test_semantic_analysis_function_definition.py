# tests/semantic_analyzer/test_semantic_analysis_function_definition.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.token import Token
from src.ast_node import ASTNode

def test_semantic_analysis_function_definition_correct(dedent_code):
    code = dedent_code("""
        def add(a, b):
            return a + b

        result = add(5, 3)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    # Assuming SemanticAnalyzer populates a symbol table
    assert analyzer.symbol_table.lookup('add') is not None
    assert analyzer.symbol_table.lookup('result') is not None

def test_semantic_analysis_function_definition_missing_return(dedent_code):
    code = dedent_code("""
        def add(a, b):
            c = a + b

        result = add(5, 3)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()
