# src/semantic_analyzer.py

from src.ast_node import ASTNode  # Import the ASTNode class

class SemanticError(Exception):
    """Custom exception for semantic analysis errors."""
    pass

class SemanticAnalyzer:
    def __init__(self):
        """
        Initialize the Semantic Analyzer with an empty symbol table.
        The symbol table keeps track of declared variables.
        """
        self.symbol_table = {}

    def analyze(self, ast):
        """
        Start the semantic analysis on the AST.
        
        :param ast: The root ASTNode representing the program.
        """
        if ast.node_type == 'PROGRAM':
            for statement in ast.children:
                self.analyze(statement)
        elif ast.node_type == 'ASSIGN':
            var_name = ast.value
            self.symbol_table[var_name] = True  # Mark variable as declared
            self.analyze(ast.children[0])  # Analyze the expression being assigned
        elif ast.node_type == 'PRINT':
            self.analyze(ast.children[0])  # Analyze the expression to be printed
        elif ast.node_type == 'BINARY_OP':
            # Analyze both operands of the binary operation
            self.analyze(ast.children[0])
            self.analyze(ast.children[1])
        elif ast.node_type == 'IDENTIFIER':
            var_name = ast.value
            if var_name not in self.symbol_table:
                raise SemanticError(f"Undeclared variable: {var_name}")
        elif ast.node_type == 'NUMBER':
            pass  # Numbers are always valid
        else:
            raise SemanticError(f"Unknown AST node type: {ast.node_type}")
