# src/semantic_analyzer.py

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        """Perform semantic analysis on the AST."""
        if node.type == "PROGRAM":
            for child in node.children:
                self.analyze(child)
        elif node.type == "ASSIGN":
            var_name = node.left.value
            self.analyze(node.right)
            self.symbol_table[var_name] = True  # Mark variable as defined
        elif node.type == "PRINT":
            self.analyze(node.left)
        elif node.type == "IDENTIFIER":
            var_name = node.value
            if var_name not in self.symbol_table:
                raise NameError(f"Undefined variable '{var_name}'")
        elif node.type in ("PLUS", "MINUS", "MULTIPLY", "DIVIDE"):
            self.analyze(node.left)
            self.analyze(node.right)
        elif node.type == "INTEGER":
            pass  # No action needed for integers
        else:
            raise SyntaxError(f"Unknown node type: {node.type}")
