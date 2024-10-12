# src/ast_node.py

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        """
        Initialize an AST node.
        
        :param node_type: The type of the node (e.g., 'ASSIGN', 'PRINT', 'BINARY_OP').
        :param value: The value associated with the node (e.g., variable name, number).
        :param children: A list of child ASTNodes.
        """
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def add_child(self, node):
        """Add a child node to the current node."""
        self.children.append(node)

    def __repr__(self):
        """Return a string representation of the ASTNode."""
        return f"ASTNode(node_type={self.node_type}, value={self.value}, children={self.children})"

    def __eq__(self, other):
        """Check equality between two ASTNodes."""
        return (
            isinstance(other, ASTNode) and 
            self.node_type == other.node_type and 
            self.value == other.value and
            self.children == other.children
        )
