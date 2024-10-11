# src/interpreter.py

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def execute(self):
        """Execute the AST."""
        self.visit(self.ast)

    def visit(self, node):
        """Visit a node."""
        if node.type == "PROGRAM":
            for child in node.children:
                self.visit(child)
        elif node.type == "ASSIGN":
            var_name = node.left.value
            var_value = self.visit(node.right)
            self.symbol_table[var_name] = var_value
        elif node.type == "PRINT":
            value = self.visit(node.left)
            print(value)
        elif node.type == "IDENTIFIER":
            var_name = node.value
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]
            else:
                raise NameError(f"Undefined variable '{var_name}'")
        elif node.type == "INTEGER":
            return node.value
        elif node.type == "PLUS":
            return self.visit(node.left) + self.visit(node.right)
        elif node.type == "MINUS":
            return self.visit(node.left) - self.visit(node.right)
        elif node.type == "MULTIPLY":
            return self.visit(node.left) * self.visit(node.right)
        elif node.type == "DIVIDE":
            denominator = self.visit(node.right)
            if denominator == 0:
                raise ZeroDivisionError("Division by zero")
            return self.visit(node.left) / denominator
        else:
            raise SyntaxError(f"Unknown node type: {node.type}")
