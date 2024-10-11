# src/ast_node.py

class ASTNode:
    def __init__(self, type_, left=None, right=None, value=None, children=None):
        self.type = type_
        self.left = left
        self.right = right
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        attrs = []
        if self.type:
            attrs.append(f"type={self.type}")
        if self.value is not None:
            attrs.append(f"value={self.value}")
        if self.left:
            attrs.append(f"left={self.left}")
        if self.right:
            attrs.append(f"right={self.right}")
        if self.children:
            attrs.append(f"children={self.children}")
        return f"ASTNode({', '.join(attrs)})"
