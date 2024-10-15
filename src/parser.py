# src/parser.py

from src.token import Token, TokenType
from src.lexer import Lexer
from src.ast_node import ASTNode

# Define custom exception for parser errors
class ParserError(Exception):
    """Custom exception for parser errors."""
    pass

class Parser:
    """Parser class for building an Abstract Syntax Tree (AST) from tokens."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def advance(self):
        """Advance the 'position' and set 'current_token'."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def parse(self):
        """Parse tokens to build an AST."""
        return self.program()

    def eat(self, token_type, value=None):
        """Consume a token of the expected type and value."""
        if self.current_token and self.current_token.type == token_type and (value is None or self.current_token.value == value):
            self.advance()
        else:
            expected = f"{token_type}" + (f" with value '{value}'" if value else "")
            actual_value = f" with value '{self.current_token.value}'" if self.current_token else 'EOF'
            actual = f"{self.current_token.type}{actual_value}" if self.current_token else 'EOF'
            raise ParserError(f"Expected {expected}, but got {actual}")

    def program(self):
        """Parse a program consisting of multiple statements."""
        statements = []
        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return ASTNode('PROGRAM', children=statements)

    def statement(self):
        if self.current_token.type == TokenType.KEYWORD:
            if self.current_token.value == 'def':
                return self.function_definition()
            elif self.current_token.value == 'try':
                return self.try_except_block()
            elif self.current_token.value == 'import':
                return self.import_statement()
            elif self.current_token.value == 'print':
                return self.print_statement()
            elif self.current_token.value == 'raise':
                return self.raise_statement()
            elif self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'while':
                return self.while_loop()
            elif self.current_token.value == 'return':
                return self.return_statement()
            elif self.current_token.value == 'pass':
                self.eat(TokenType.KEYWORD, 'pass')
                return ASTNode('PASS')
            else:
                raise ParserError(f"Unexpected keyword: {self.current_token.value}")
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment_or_function_call()
        else:
            raise ParserError(f"Unexpected token: {self.current_token.type} ({self.current_token.value})")
            
    def return_statement(self):
        self.eat(TokenType.KEYWORD, 'return')
        if self.current_token.type != TokenType.KEYWORD and self.current_token.type != TokenType.EOF:
            expr = self.expression()
            return ASTNode('RETURN', children=[expr])
        else:
            return ASTNode('RETURN')

    def assignment_or_function_call(self):
        """Parse an assignment or function call."""
        if self.lookahead_is_assignment():
            return self.assignment()
        else:
            return self.function_call_statement()

    def lookahead_is_assignment(self):
        """Check if the current position indicates an assignment."""
        next_position = self.position + 1
        if next_position < len(self.tokens):
            next_token = self.tokens[next_position]
            return next_token.type == TokenType.SPECIAL_CHAR and next_token.value == '='
        return False

    def assignment(self):
        """Parse an assignment statement."""
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SPECIAL_CHAR, '=')
        expr = self.expression()
        return ASTNode('ASSIGN', value=var_name, children=[expr])

    def function_call_statement(self):
        """Parse a function call as a statement."""
        func_call = self.function_call()
        return ASTNode('EXPRESSION_STATEMENT', children=[func_call])

    def print_statement(self):
        """Parse a print statement."""
        self.eat(TokenType.KEYWORD, 'print')
        self.eat(TokenType.SPECIAL_CHAR, '(')
        expr = self.expression()
        self.eat(TokenType.SPECIAL_CHAR, ')')
        return ASTNode('PRINT', children=[expr])

    def function_definition(self):
        """Parse a function definition."""
        self.eat(TokenType.KEYWORD, 'def')
        func_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SPECIAL_CHAR, '(')
        params = []
        if self.current_token.type != TokenType.SPECIAL_CHAR or self.current_token.value != ')':
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == ',':
                self.eat(TokenType.SPECIAL_CHAR, ',')
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SPECIAL_CHAR, ')')
        self.eat(TokenType.SPECIAL_CHAR, ':')
        body = []
        while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'end'):
            stmt = self.statement()
            body.append(stmt)
        self.eat(TokenType.KEYWORD, 'end')
        return ASTNode('FUNCTION_DEF', value=func_name, children=[
            ASTNode('PARAMS', value=params),
            ASTNode('BODY', children=body)
        ])

    def try_except_block(self):
        self.eat(TokenType.KEYWORD, 'try')
        self.eat(TokenType.SPECIAL_CHAR, ':')
        try_body = []
        while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'except'):
            stmt = self.statement()
            try_body.append(stmt)
        except_clauses = []
        while self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'except':
            self.eat(TokenType.KEYWORD, 'except')
            exception_type = None
            if self.current_token.type == TokenType.IDENTIFIER:
                exception_type = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.SPECIAL_CHAR, ':')
            except_body = []
            while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value in ('except', 'end')):
                stmt = self.statement()
                except_body.append(stmt)
            except_clauses.append(ASTNode('EXCEPT_CLAUSE', value=exception_type, children=[
                ASTNode('BODY', children=except_body)
            ]))
        self.eat(TokenType.KEYWORD, 'end')
        return ASTNode('TRY_EXCEPT', children=[
            ASTNode('TRY_BODY', children=try_body),
            ASTNode('EXCEPT_CLAUSES', children=except_clauses)
        ])

    def import_statement(self):
        """Parse an import statement."""
        self.eat(TokenType.KEYWORD, 'import')
        module_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        return ASTNode('IMPORT', value=module_name)

    def raise_statement(self):
        self.eat(TokenType.KEYWORD, 'raise')
        if self.current_token.type == TokenType.IDENTIFIER:
            exception_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == '(':
                self.eat(TokenType.SPECIAL_CHAR, '(')
                args = []
                if self.current_token.type != TokenType.SPECIAL_CHAR or self.current_token.value != ')':
                    args.append(self.expression())
                    while self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == ',':
                        self.eat(TokenType.SPECIAL_CHAR, ',')
                        args.append(self.expression())
                self.eat(TokenType.SPECIAL_CHAR, ')')
                return ASTNode('RAISE', value=exception_name, children=args)
            else:
                return ASTNode('RAISE', value=exception_name)
        else:
            raise ParserError(f"Expected exception name after 'raise', but got {self.current_token.type}")

    def if_statement(self):
        """Parse an if statement."""
        self.eat(TokenType.KEYWORD, 'if')
        condition = self.expression()
        self.eat(TokenType.SPECIAL_CHAR, ':')
        body = []
        while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value in ('else', 'end')):
            stmt = self.statement()
            body.append(stmt)
        else_body = []
        if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
            self.eat(TokenType.KEYWORD, 'else')
            self.eat(TokenType.SPECIAL_CHAR, ':')
            while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'end'):
                stmt = self.statement()
                else_body.append(stmt)
        self.eat(TokenType.KEYWORD, 'end')
        return ASTNode('IF', children=[
            condition,
            ASTNode('BODY', children=body),
            ASTNode('ELSE_BODY', children=else_body)
        ])

    def while_loop(self):
        """Parse a while loop."""
        self.eat(TokenType.KEYWORD, 'while')
        condition = self.expression()
        self.eat(TokenType.SPECIAL_CHAR, ':')
        body = []
        while self.current_token and not (self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'end'):
            stmt = self.statement()
            body.append(stmt)
        self.eat(TokenType.KEYWORD, 'end')
        return ASTNode('WHILE', children=[
            condition,
            ASTNode('BODY', children=body)
        ])

    def expression(self):
        """Parse an expression."""
        return self.logical_or()

    def logical_or(self):
        """Parse logical OR expressions."""
        node = self.logical_and()
        while self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'or':
            op = self.current_token.value
            self.eat(TokenType.KEYWORD, 'or')
            node = ASTNode('BIN_OP', value=op, children=[node, self.logical_and()])
        return node

    def logical_and(self):
        """Parse logical AND expressions."""
        node = self.equality()
        while self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'and':
            op = self.current_token.value
            self.eat(TokenType.KEYWORD, 'and')
            node = ASTNode('BIN_OP', value=op, children=[node, self.equality()])
        return node

    def equality(self):
        """Parse equality expressions."""
        node = self.relational()
        while self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value in ('==', '!='):
            op = self.current_token.value
            self.eat(TokenType.SPECIAL_CHAR)
            node = ASTNode('BIN_OP', value=op, children=[node, self.relational()])
        return node

    def relational(self):
        """Parse relational expressions."""
        node = self.term()
        while self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value in ('<', '<=', '>', '>='):
            op = self.current_token.value
            self.eat(TokenType.SPECIAL_CHAR)
            node = ASTNode('BIN_OP', value=op, children=[node, self.term()])
        return node

    def term(self):
        """Parse a term in an expression."""
        node = self.factor()
        while self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value in ('+', '-'):
            op = self.current_token.value
            self.eat(TokenType.SPECIAL_CHAR)
            node = ASTNode('BIN_OP', value=op, children=[node, self.factor()])
        return node

    def factor(self):
        """Parse a factor in an expression."""
        node = self.unary()
        while self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value in ('*', '/', '%'):
            op = self.current_token.value
            self.eat(TokenType.SPECIAL_CHAR)
            node = ASTNode('BIN_OP', value=op, children=[node, self.unary()])
        return node

    def unary(self):
        """Parse a unary operation."""
        if self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == '-':
            op = self.current_token.value
            self.eat(TokenType.SPECIAL_CHAR)
            node = ASTNode('UNARY_OP', value=op, children=[self.unary()])
            return node
        return self.primary()

    def primary(self):
        """Parse a primary expression."""
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return ASTNode('NUMBER', value=token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return ASTNode('STRING', value=token.value)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return ASTNode('BOOLEAN', value=token.value)    
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            node = ASTNode('VARIABLE', value=token.value)
            while self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == '.':
                self.eat(TokenType.SPECIAL_CHAR, '.')
                attr_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                node = ASTNode('ATTRIBUTE_ACCESS', value=attr_name, children=[node])
            if self.current_token and self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == '(':
                # Function call
                return self.finish_function_call(node)
            else:
                return node
        elif token.type == TokenType.SPECIAL_CHAR and token.value == '(':
            self.eat(TokenType.SPECIAL_CHAR, '(')
            node = self.expression()
            self.eat(TokenType.SPECIAL_CHAR, ')')
            return node
        else:
            raise ParserError(f"Unexpected token: {token.type} ({token.value})")

    def function_call(self):
        """Parse a function call expression."""
        func_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        node = ASTNode('VARIABLE', value=func_name)
        return self.finish_function_call(node)

    def finish_function_call(self, node):
        """Finish parsing a function call after the function name or attribute access."""
        self.eat(TokenType.SPECIAL_CHAR, '(')
        args = []
        if self.current_token.type != TokenType.SPECIAL_CHAR or self.current_token.value != ')':
            args.append(self.expression())
            while self.current_token.type == TokenType.SPECIAL_CHAR and self.current_token.value == ',':
                self.eat(TokenType.SPECIAL_CHAR, ',')
                args.append(self.expression())
        self.eat(TokenType.SPECIAL_CHAR, ')')
        return ASTNode('FUNCTION_CALL', value=node, children=args)
        
    def visit_boolean(self, node):
        pass  # Booleans are always valid

    def visit_return(self, node):
        if node.children:
            self.visit(node.children[0])  # Visit the return expression

    def visit_attribute_access(self, node):
        # For nodes like module.function
        self.visit(node.children[0])  # Visit the object/module
        # node.value is the attribute name; you might need additional handling
        
    def visit_function_call(self, node):
        func_node = node.value
        func_name = func_node.value
        if func_node.type == 'ATTRIBUTE_ACCESS':
            # Handle module or object methods
            self.visit(func_node)
        elif not self.is_variable_declared(func_name):
            raise SemanticError(f"Function '{func_name}' is not defined")
        # Check for correct number of arguments if you have function definitions stored
        for arg in node.children:
            self.visit(arg)

