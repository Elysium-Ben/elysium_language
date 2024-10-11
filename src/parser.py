# src/parser.py

from src.ast_node import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def advance(self):
        """Advance to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Parse the tokens and return the AST."""
        if not self.tokens:
            return None
        return self.program()

    def program(self):
        """Parse a sequence of statements."""
        statements = []
        while self.current_token.type != "EOF":
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return ASTNode("PROGRAM", children=statements)

    def statement(self):
        """Parse a single statement."""
        if self.current_token.type == "IDENTIFIER":
            return self.assignment()
        elif self.current_token.type == "PRINT":
            return self.print_statement()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type}")

    def assignment(self):
        """Parse an assignment statement."""
        var_name = self.current_token.value
        self.advance()
        if self.current_token.type != "ASSIGN":
            raise SyntaxError("Expected '=' after identifier")
        self.advance()
        expr = self.expression()
        return ASTNode("ASSIGN", left=ASTNode("IDENTIFIER", value=var_name), right=expr)

    def print_statement(self):
        """Parse a print statement."""
        self.advance()
        if self.current_token.type != "LPAREN":
            raise SyntaxError("Expected '(' after 'print'")
        self.advance()
        expr = self.expression()
        if self.current_token.type != "RPAREN":
            raise SyntaxError("Expected ')' after expression")
        self.advance()
        return ASTNode("PRINT", left=expr)

    def expression(self):
        """Parse an expression."""
        node = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token
            self.advance()
            node = ASTNode(token.type, left=node, right=self.term())
        return node

    def term(self):
        """Parse a term."""
        node = self.factor()
        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            token = self.current_token
            self.advance()
            node = ASTNode(token.type, left=node, right=self.factor())
        return node

    def factor(self):
        """Parse a factor."""
        token = self.current_token
        if token.type == "INTEGER":
            self.advance()
            return ASTNode("INTEGER", value=token.value)
        elif token.type == "IDENTIFIER":
            self.advance()
            return ASTNode("IDENTIFIER", value=token.value)
        elif token.type == "LPAREN":
            self.advance()
            node = self.expression()
            if self.current_token.type != "RPAREN":
                raise SyntaxError("Expected ')' after expression")
            self.advance()
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")
