# src/token.py

class Token:
    def __init__(self, token_type, value, position=None):
        """
        Initialize a Token.
        
        :param token_type: The type of the token (e.g., 'IDENTIFIER', 'NUMBER').
        :param value: The value of the token (e.g., variable name, numerical value).
        :param position: The position of the token in the input (optional).
        """
        self.token_type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        """Return a string representation of the Token."""
        return f"Token(type={self.token_type}, value={self.value}, position={self.position})"

    def __eq__(self, other):
        """Check equality between two Tokens."""
        return (
            isinstance(other, Token) and 
            self.token_type == other.token_type and 
            self.value == other.value and 
            self.position == other.position
        )
