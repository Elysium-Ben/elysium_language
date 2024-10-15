# src/interpreter.py

class InterpreterError(Exception):
    """Exception raised for errors during interpretation."""
    pass


class ReturnException(Exception):
    """Exception used to handle return statements in functions."""
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.scopes = [{}]  # Initialize with the global scope
        self.functions = {}  # Store function definitions
        self.imported_modules = set()  # Store imported modules

    def interpret(self, ast):
        try:
            self.visit(ast)
        except Exception as e:
            raise InterpreterError(f"Unhandled exception: {e}")

    def visit(self, node):
        method_name = 'visit_' + node.type.upper().replace('-', '_').replace(' ', '_')
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise InterpreterError(f"No {method_name} method defined")
        return visitor(node)

    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)

    def visit_ASSIGN(self, node):
        var_name = node.value
        value = self.visit(node.children[0])
        self.current_scope()[var_name] = value

    def visit_NUMBER(self, node):
        return node.value

    def visit_STRING(self, node):
        return node.value

    def visit_BOOLEAN(self, node):
        return node.value

    def visit_VARIABLE(self, node):
        var_name = node.value
        value = self.lookup_variable(var_name)
        if value is None:
            raise InterpreterError(f"Variable '{var_name}' is not defined")
        return value

    def visit_BIN_OP(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        op = node.value
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        else:
            raise InterpreterError(f"Unknown operator: {op}")

    def visit_UNARY_OP(self, node):
        operand = self.visit(node.children[0])
        op = node.value
        if op == '+':
            return +operand
        elif op == '-':
            return -operand
        else:
            raise InterpreterError(f"Unknown unary operator: {op}")

    def visit_PRINT(self, node):
        value = self.visit(node.children[0])
        print(value)

    def visit_IF(self, node):
        condition = self.visit(node.children[0])
        if condition:
            # Create a new scope for the if body
            self.scopes.append({})
            self.visit(node.children[1])  # If body
            self.scopes.pop()
        elif len(node.children) > 2:
            # Create a new scope for the else body
            self.scopes.append({})
            self.visit(node.children[2])  # Else body
            self.scopes.pop()

    def visit_ELSE_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_WHILE(self, node):
        condition_node = node.children[0]
        body_node = node.children[1]
        iterations = 0
        MAX_LOOP_ITERATIONS = 1000
        while self.visit(condition_node):
            if iterations >= MAX_LOOP_ITERATIONS:
                raise InterpreterError("Maximum loop iterations exceeded")
            # Create a new scope for the loop body
            self.scopes.append({})
            self.visit(body_node)
            self.scopes.pop()
            iterations += 1

    def visit_FUNCTION_DEF(self, node):
        func_name = node.value
        params = node.children[0].value  # List of parameter names
        body = node.children[1]
        self.functions[func_name] = {
            'params': params,
            'body': body
        }

    def visit_FUNCTION_CALL(self, node):
        func_node = node.value
        if func_node.type == 'VARIABLE':
            func_name = func_node.value
            if func_name in self.functions:
                func_def = self.functions[func_name]
                expected_arg_count = len(func_def['params'])
                actual_arg_count = len(node.children)
                if expected_arg_count != actual_arg_count:
                    raise InterpreterError(f"Function '{func_name}' expects {expected_arg_count} arguments but {actual_arg_count} were given")
                args = [self.visit(arg) for arg in node.children]
                # Create a new scope for the function call
                new_scope = {}
                for param, arg in zip(func_def['params'], args):
                    new_scope[param] = arg
                self.scopes.append(new_scope)
                try:
                    self.visit(func_def['body'])
                except ReturnException as e:
                    self.scopes.pop()
                    return e.value
                self.scopes.pop()
            elif func_name in self.get_builtin_functions():
                # Handle built-in functions
                args = [self.visit(arg) for arg in node.children]
                return self.execute_builtin_function(func_name, args)
            else:
                raise InterpreterError(f"Function '{func_name}' is not defined")
        elif func_node.type == 'ATTRIBUTE_ACCESS':
            module_node = func_node.children[0]
            module_name = module_node.value
            function_name = func_node.value
            if module_name not in self.imported_modules:
                raise InterpreterError(f"Module '{module_name}' is not imported")
            # Handle module functions
            if module_name == 'math':
                if function_name == 'add':
                    if len(node.children) != 2:
                        raise InterpreterError(f"Function 'add' expects 2 arguments but {len(node.children)} were given")
                    a = self.visit(node.children[0])
                    b = self.visit(node.children[1])
                    return a + b
                else:
                    raise InterpreterError(f"Function '{function_name}' not found in module '{module_name}'")
            else:
                raise InterpreterError(f"Module '{module_name}' has no function '{function_name}'")
        else:
            raise InterpreterError(f"Unknown function node type: {func_node.type}")

    def visit_RETURN(self, node):
        if node.children:
            value = self.visit(node.children[0])
            raise ReturnException(value)
        else:
            raise ReturnException(None)

    def visit_EXPRESSION_STATEMENT(self, node):
        self.visit(node.children[0])

    def visit_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_TRY_EXCEPT(self, node):
        try:
            self.visit(node.children[0])  # TRY_BODY
        except Exception as e:
            handled = False
            for except_clause in node.children[1].children:
                exception_type = except_clause.value
                if exception_type is None or isinstance(e, self.get_exception_class(exception_type)):
                    self.visit(except_clause.children[0])  # BODY
                    handled = True
                    break
            if not handled:
                raise e  # Re-raise the exception if not handled

    def visit_TRY_BODY(self, node):
        for child in node.children:
            self.visit(child)

    def visit_EXCEPT_CLAUSES(self, node):
        for child in node.children:
            self.visit(child)

    def visit_EXCEPT_CLAUSE(self, node):
        # node.value contains the exception type (can be None)
        self.visit(node.children[0])  # BODY node

    def visit_RAISE(self, node):
        if node.children:
            exception_name = node.value
            self.visit(node.children[0])  # Exception expression
            raise self.get_exception_class(exception_name)()

    def visit_PASS(self, node):
        pass  # Do nothing

    def visit_IMPORT(self, node):
        module_name = node.value
        # For simplicity, only allow 'math' module
        if module_name not in {'math'}:
            raise SemanticError(f"Module '{module_name}' not found")
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
        return func_name in self.functions or func_name in self.get_builtin_functions()

    def current_scope(self):
        return self.scopes[-1]

    def get_builtin_functions(self):
        return {'int', 'str', 'print', 'len'}

    def execute_builtin_function(self, func_name, args):
        if func_name == 'int':
            if len(args) != 1:
                raise InterpreterError(f"Function 'int' expects 1 argument but {len(args)} were given")
            return int(args[0])
        elif func_name == 'str':
            if len(args) != 1:
                raise InterpreterError(f"Function 'str' expects 1 argument but {len(args)} were given")
            return str(args[0])
        elif func_name == 'print':
            print(*args)
            return None
        elif func_name == 'len':
            if len(args) != 1:
                raise InterpreterError(f"Function 'len' expects 1 argument but {len(args)} were given")
            return len(args[0])
        else:
            raise InterpreterError(f"Unknown built-in function: {func_name}")

    def get_exception_class(self, exception_name):
        # Map exception names to actual exception classes
        return {
            'Exception': Exception,
            'ValueError': ValueError,
            'TypeError': TypeError,
            'ZeroDivisionError': ZeroDivisionError,
            # Add other exceptions as needed
        }.get(exception_name, Exception)

    def lookup_variable(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name]
        return None
