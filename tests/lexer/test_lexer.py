# tests/lexer/test_lexer.py

import pytest
from src.lexer import Lexer  # Import the Lexer class
from src.token import Token  # Import the Token class

@pytest.fixture
def dedent_code():
    """Fixture to dedent multiline code strings."""
    import textwrap
    def _dedent_code(code):
        return textwrap.dedent(code).strip()
    return _dedent_code

def test_lexer_basic(dedent_code, capfd):
    """Test the lexer's ability to tokenize a basic set of statements."""
    code = dedent_code("""
        x = 10
        y = x + 5
        print(y)
    """)
    print(f"Processed Code:\n{repr(code)}\n")  # Debugging statement
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"Generated Tokens:\n{tokens}\n")    # Debugging statement

    expected_tokens = [
        Token(token_type='IDENTIFIER', value='x'),
        Token(token_type='ASSIGN', value='='),
        Token(token_type='NUMBER', value=10),
        Token(token_type='NEWLINE', value='\n'),
        Token(token_type='IDENTIFIER', value='y'),
        Token(token_type='ASSIGN', value='='),
        Token(token_type='IDENTIFIER', value='x'),
        Token(token_type='PLUS', value='+'),
        Token(token_type='NUMBER', value=5),
        Token(token_type='NEWLINE', value='\n'),
        Token(token_type='PRINT', value='print'),
        Token(token_type='LPAREN', value='('),
        Token(token_type='IDENTIFIER', value='y'),
        Token(token_type='RPAREN', value=')'),
        Token(token_type='EOF', value=None)
    ]
    assert tokens == expected_tokens
