# src/interpreter.py

class InterpreterError(Exception):
    """Base class for interpreter-specific errors."""
    pass


class InfiniteLoopError(InterpreterError):
    """Raised when an infinite loop is detected."""
    pass


class InfiniteRecursionError(InterpreterError):
    """Raised when infinite recursion is detected."""
    pass


class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def execute(self):
        """Executes the AST."""
        self.visit(self.ast)

    def visit(self, node):
        """Visits a node and calls the appropriate method."""
        method_name = f"visit_{node.node_type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        raise InterpreterError(f'No visit_{node.node_type} method')

    # Example method to handle a 'PROGRAM' node
    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)

    # You can add more visit methods here, depending on the node types in your AST.
