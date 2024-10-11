# src/ast_node.py

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"ASTNode(node_type={self.node_type}, value={self.value}, children={self.children})"

    def __eq__(self, other):
        return (
            isinstance(other, ASTNode) and 
            self.node_type == other.node_type and 
            self.value == other.value and
            self.children == other.children
        )
