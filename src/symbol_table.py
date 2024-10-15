# src/symbol_table.py

class SymbolTable:
    """Symbol table to keep track of variable and function declarations."""

    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def set(self, name, value):
        """Set a symbol in the current scope."""
        self.symbols[name] = value

    def get(self, name):
        """Get a symbol from the current scope or parent scopes."""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None
