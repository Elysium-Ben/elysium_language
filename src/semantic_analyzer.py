# src/semantic_analyzer.py

from src.ast_node import ASTNode
from src.token import Token

class SemanticError(Exception):
    """Exception raised for semantic analysis errors."""
    pass

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
    
    def analyze(self):
        self.visit(self.ast)
    
    def visit(self, node):
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise SemanticError(f"No visit_{node.node_type} method")
    
    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_ASSIGN(self, node):
        var_name = node.value
        value = self.visit(node.children[0])
        if var_name in self.symbol_table:
            raise SemanticError(f"Duplicate variable declaration: '{var_name}'")
        self.symbol_table[var_name] = value
    
    def visit_PRINT(self, node):
        # Assuming SemanticAnalyzer doesn't handle print semantics
        pass
    
    def visit_INTEGER(self, node):
        return node.value
    
    def visit_IDENTIFIER(self, node):
        var_name = node.value
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        else:
            raise SemanticError(f"Undeclared variable: '{var_name}'")
    
    def visit_BIN_OP(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        op = node.value
    
        if op in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            return  # For semantic analysis, you might check operand types
        else:
            raise SemanticError(f"Unknown binary operator: '{op}'")
    
    def visit_TRY_EXCEPT(self, node):
        self.visit(node.children[0])  # Try block
        self.visit(node.children[1])  # Except block
    # Add other visit methods as needed
