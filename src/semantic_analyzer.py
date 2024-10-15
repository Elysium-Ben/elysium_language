# src/semantic_analyzer.py

class SemanticError(Exception):
    """Exception raised for semantic errors in the code."""
    pass


class SemanticAnalyzer:
    """Semantic Analyzer class for semantic checks."""

    def __init__(self, allow_function_overwrite=False):
        self.scopes = [{}]  # Stack of scopes; start with global scope
        self.functions = {}  # Map function names to parameter counts
        self.allow_function_overwrite = allow_function_overwrite
        self.imported_modules = set()  # Set of imported module names

    def visit(self, node):
        method_name = 'visit_' + node.type.upper().replace('-', '_').replace(' ', '_')
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise SemanticError(f"Unknown node type: {node.type}")
        return visitor(node)

    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)

    def visit_ASSIGN(self, node):
        var_name = node.value
        self.visit(node.children[0])  # Visit the expression on the right-hand side
        self.current_scope()[var_name] = True  # Declare the variable in the current scope

    def visit_NUMBER(self, node):
        pass  # Numbers are always valid

    def visit_STRING(self, node):
        pass  # Strings are always valid

    def visit_BOOLEAN(self, node):
        pass  # Booleans are always valid

    def visit_VARIABLE(self, node):
        var_name = node.value
        if not self.is_variable_declared(var_name):
            raise SemanticError(f"Undeclared variable: {var_name}")

    def visit_BIN_OP(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def visit_UNARY_OP(self, node):
        self.visit(node.children[0])

    def visit_FUNCTION_DEF(self, node):
        func_name = node.value
        params = node.children[0].value  # List of parameter names
        if not self.allow_function_overwrite and func_name in self.functions:
            raise SemanticError(f"Function '{func_name}' is already defined")
        self.functions[func_name] = len(params)
        self.current_scope()[func_name] = True  # Declare the function in the current scope
        # Create a new scope for the function
        self.scopes.append({})
        # Add parameters to the function scope
        for param in params:
            self.current_scope()[param] = True
        # Visit the function body
        self.visit(node.children[1])  # BODY node
        # Pop the function scope
        self.scopes.pop()

    def visit_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_RETURN(self, node):
        if node.children:
            self.visit(node.children[0])  # Return expression

    def visit_PRINT(self, node):
        self.visit(node.children[0])

    def visit_IF(self, node):
        self.visit(node.children[0])  # Condition
        # Create a new scope for the if body
        self.scopes.append({})
        self.visit(node.children[1])  # If body
        self.scopes.pop()
        if len(node.children) > 2:
            # Create a new scope for the else body
            self.scopes.append({})
            self.visit(node.children[2])  # Else body
            self.scopes.pop()

    def visit_ELSE_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_WHILE(self, node):
        self.visit(node.children[0])  # Condition
        # Create a new scope for the loop body
        self.scopes.append({})
        self.visit(node.children[1])  # Loop body
        self.scopes.pop()

    def visit_TRY_EXCEPT(self, node):
        self.visit(node.children[0])  # TRY_BODY
        self.visit(node.children[1])  # EXCEPT_CLAUSES

    def visit_TRY_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_EXCEPT_CLAUSES(self, node):
        for child in node.children:
            self.visit(child)

    def visit_EXCEPT_CLAUSE(self, node):
        # node.value contains the exception type (can be None)
        # Create a new scope for the except body
        self.scopes.append({})
        self.visit(node.children[0])  # BODY node
        self.scopes.pop()

    def visit_RAISE(self, node):
        if node.children:
            self.visit(node.children[0])  # Exception expression

    def visit_FUNCTION_CALL(self, node):
        func_node = node.value
        if func_node.type == 'VARIABLE':
            func_name = func_node.value
            if func_name in self.functions:
                expected_arg_count = self.functions[func_name]
                actual_arg_count = len(node.children)
                if expected_arg_count != actual_arg_count:
                    raise SemanticError(f"Function '{func_name}' expects {expected_arg_count} arguments but {actual_arg_count} were given")
            elif not self.is_variable_declared(func_name):
                raise SemanticError(f"Function '{func_name}' is not defined")
        elif func_node.type == 'ATTRIBUTE_ACCESS':
            # Handle module function calls
            module_node = func_node.children[0]
            module_name = module_node.value
            function_name = func_node.value
            if module_name not in self.imported_modules:
                raise SemanticError(f"Module '{module_name}' not imported")
            # Assume functions from imported modules are valid
        else:
            raise SemanticError(f"Unknown function node type: {func_node.type}")
        for arg in node.children:
            self.visit(arg)

    def visit_EXPRESSION_STATEMENT(self, node):
        self.visit(node.children[0])

    def visit_PASS(self, node):
        pass  # Do nothing

    def visit_IMPORT(self, node):
        module_name = node.value
        # For simplicity, assume module exists
        self.imported_modules.add(module_name)

    def visit_ATTRIBUTE_ACCESS(self, node):
        module_node = node.children[0]
        module_name = module_node.value
        if module_name not in self.imported_modules:
            raise SemanticError(f"Module '{module_name}' not imported")
        # Assume attributes from imported modules are valid

    def is_variable_declared(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return True
        return False

    def is_function_defined(self, func_name):
        return func_name in self.functions

    def current_scope(self):
        return self.scopes[-1]
