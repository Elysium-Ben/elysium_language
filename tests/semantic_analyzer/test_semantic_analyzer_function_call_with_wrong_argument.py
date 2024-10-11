# tests/semantic_analyzer/test_semantic_analyzer_function_call_with_wrong_argument.py

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError
from src.token import Token
from src.ast_node import ASTNode

def test_function_call_with_wrong_number_of_arguments(dedent_code):
    code = dedent_code("""
        def multiply(a, b):
            return a * b

        result = multiply(5)  # Missing second argument
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(ast)
    with pytest.raises(SemanticError):
        analyzer.analyze()
