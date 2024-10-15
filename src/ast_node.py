# src/ast_node.py

class ASTNode:
    """Class representing a node in the Abstract Syntax Tree (AST)."""

    def __init__(self, node_type, value=None, children=None):
        self.type = node_type      # The type of the node (e.g., 'PROGRAM', 'ASSIGN')
        self.value = value         # The value associated with the node (e.g., variable name)
        self.children = children if children is not None else []  # List of child nodes

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value}, children={self.children})"

    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        return (self.type == other.type and
                self.value == other.value and
                self.children == other.children)

    def __hash__(self):
        # Ensure all children are hashable; convert lists to tuples
        return hash((self.type, self.value, tuple(self.children)))
