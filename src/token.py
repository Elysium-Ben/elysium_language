# src/token.py

class Token:
    def __init__(self, token_type, value=None, position=None):
        self.token_type = token_type  # The type of the token (e.g., 'IDENTIFIER', 'ASSIGN')
        self.value = value            # The actual value of the token (e.g., variable name or number)
        self.position = position      # Optional: position of the token in the source code for error reporting

    def __repr__(self):
        return f"Token(type={self.token_type}, value={self.value}, position={self.position})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (
            self.token_type == other.token_type and
            self.value == other.value and
            self.position == other.position
        )
