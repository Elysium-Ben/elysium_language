# src/symbol_table.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise NameError(f"Undefined variable '{name}'")
