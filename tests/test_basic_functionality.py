# tests/test_basic_functionality.py

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter

def test_basic_assignment_and_print(capfd, dedent_code):
    code = dedent_code("""
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
    interpreter = Interpreter(ast)
    interpreter.execute()
    captured = capfd.readouterr()
    assert captured.out.strip() == "15"
