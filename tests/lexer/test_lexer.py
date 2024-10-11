# tests/lexer/test_lexer.py

from src.lexer import Lexer, Token

def test_basic_lexing(dedent_code):
    code = dedent_code("""
        x = 10
        y = x + 5
        print(y)
    """)
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    expected_tokens = [
        Token("IDENTIFIER", "x"),
        Token("ASSIGN"),
        Token("INTEGER", 10),
        Token("IDENTIFIER", "y"),
        Token("ASSIGN"),
        Token("IDENTIFIER", "x"),
        Token("PLUS"),
        Token("INTEGER", 5),
        Token("PRINT"),
        Token("LPAREN"),
        Token("IDENTIFIER", "y"),
        Token("RPAREN"),
        Token("EOF")
    ]
    print(f"Actual Tokens: {tokens}")       # Debug print
    print(f"Expected Tokens: {expected_tokens}")  # Debug print
    assert tokens == expected_tokens
