from src.token import Token
from src.ast_node import ASTNode  # Importing ASTNode

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def advance(self):
        """Advance to the next token in the input"""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token('EOF', None)  # Handle end of token stream

    def error(self, message):
        raise SyntaxError(message)

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.advance()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.token_type}")

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token.token_type != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return ASTNode('PROGRAM', children=statements)

    def statement(self):
        if self.current_token.token_type == 'IDENTIFIER':
            return self.assignment()
        elif self.current_token.token_type == 'PRINT':
            return self.print_statement()
        elif self.current_token.token_type == 'DEF':
            return self.function_definition()
        elif self.current_token.token_type == 'TRY':
            return self.try_except_statement()
        else:
            self.error(f"Unexpected token: {self.current_token.token_type}")

    def assignment(self):
        left = self.current_token
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        right = self.expression()
        return ASTNode('ASSIGN', value=left.value, children=[right])

    def print_statement(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        return ASTNode('PRINT', children=[expr])

    def function_definition(self):
        self.eat('DEF')
        func_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        params = self.parameter_list()
        self.eat('RPAREN')
        body = self.block()
        return ASTNode('FUNCTION_DEF', children=[func_name, params, body])

    def parameter_list(self):
        params = []
        if self.current_token.token_type == 'IDENTIFIER':
            params.append(self.current_token.value)
            self.eat('IDENTIFIER')
            while self.current_token.token_type == 'COMMA':
                self.eat('COMMA')
                params.append(self.current_token.value)
                self.eat('IDENTIFIER')
        return params

    def block(self):
        block_statements = []
        while self.current_token.token_type not in {'EXCEPT', 'EOF', 'DEDENT'}:
            block_statements.append(self.statement())
        return ASTNode('BLOCK', children=block_statements)

    def try_except_statement(self):
        self.eat('TRY')
        try_block = self.block()
        self.eat('EXCEPT')
        except_block = self.block()
        return ASTNode('TRY_EXCEPT', children=[try_block, except_block])

    def expression(self):
        expr = self.current_token
        self.advance()
        return ASTNode(expr.token_type, value=expr.value)
