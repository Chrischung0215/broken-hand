from ast import *
from error import BrokenHandError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, msg='Syntax error'):
        raise BrokenHandError(f"{msg} at position {self.pos}, token: {self.current_token}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
            self.skip_newlines()
        else:
            self.error(f"Expected token {token_type} but got {self.current_token.type}")

    def skip_newlines(self):
        while self.current_token.type == 'NEWLINE':
            self.advance()

    def parse(self):
        statements = []
        self.skip_newlines()
        while self.current_token.type != 'EOF':
            statements.append(self.statement())
            self.skip_newlines()
        return Program(statements)

    def statement(self):
        if self.current_token.type == 'ID':
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type == 'ASSIGN':
                return self.assignment()
            else:
                expr = self.expr()
                return expr
        elif self.current_token.type == 'PRINT':
            return self.print_stmt()
        elif self.current_token.type == 'IF':
            return self.if_stmt()
        elif self.current_token.type == 'WHILE':
            return self.while_stmt()
        elif self.current_token.type == 'FUNCTION':
            return self.function_def()
        elif self.current_token.type == 'RETURN':
            return self.return_stmt()
        else:
            expr = self.expr()
            return expr

    def assignment(self):
        var_name = self.current_token.value
        self.eat('ID')
        self.eat('ASSIGN')
        expr_node = self.expr()
        return Assign(var_name, expr_node)

    def print_stmt(self):
        self.eat('PRINT')
        expr_node = self.expr()
        return Print(expr_node)

    def if_stmt(self):
        self.eat('IF')
        self.eat('LPAREN')
        cond = self.expr()
        self.eat('RPAREN')
        self.eat('LBRACE')
        then_body = []
        while self.current_token.type != 'RBRACE':
            then_body.append(self.statement())
        self.eat('RBRACE')

        else_body = None
        # 判斷是否有 else
        if self.current_token.type == 'ID' and self.current_token.value == 'else':
            self.eat('ID')
            self.eat('LBRACE')
            else_body = []
            while self.current_token.type != 'RBRACE':
                else_body.append(self.statement())
            self.eat('RBRACE')

        return If(cond, then_body, else_body)

    def while_stmt(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        cond = self.expr()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body_stmts = []
        while self.current_token.type != 'RBRACE':
            body_stmts.append(self.statement())
        self.eat('RBRACE')
        return While(cond, body_stmts)

    def function_def(self):
        self.eat('FUNCTION')
        func_name = self.current_token.value
        self.eat('ID')
        self.eat('LPAREN')
        params = []
        if self.current_token.type == 'ID':
            params.append(self.current_token.value)
            self.eat('ID')
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                params.append(self.current_token.value)
                self.eat('ID')
        self.eat('RPAREN')
        self.eat('LBRACE')
        body_stmts = []
        while self.current_token.type != 'RBRACE':
            body_stmts.append(self.statement())
        self.eat('RBRACE')
        return FunctionDef(func_name, params, body_stmts)

    def return_stmt(self):
        self.eat('RETURN')
        expr_node = self.expr()
        return Return(expr_node)

    def expr(self):
        return self.logic_or()

    def logic_or(self):
        node = self.logic_and()
        while self.current_token.type == 'OR':
            token = self.current_token
            self.eat('OR')
            node = BinOp(left=node, op=token.type, right=self.logic_and())
        return node

    def logic_and(self):
        node = self.equality()
        while self.current_token.type == 'AND':
            token = self.current_token
            self.eat('AND')
            node = BinOp(left=node, op=token.type, right=self.equality())
        return node

    def equality(self):
        node = self.relational()
        while self.current_token.type in ('EQ', 'NE'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.type, right=self.relational())
        return node

    def relational(self):
        node = self.additive()
        while self.current_token.type in ('LT', 'GT', 'LE', 'GE'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.type, right=self.additive())
        return node

    def additive(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.type, right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.type, right=self.factor())
        return node

    def factor(self):
        self.skip_newlines()
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        elif token.type == 'BOOLEAN':
            val = token.value
            self.eat('BOOLEAN')
            return Boolean(val)
        elif token.type == 'STRING':
            val = token.value
            self.eat('STRING')
            return String(val)
        elif token.type == 'ID':
            id_name = token.value
            self.eat('ID')
            if self.current_token.type == 'LPAREN':
                self.eat('LPAREN')
                args = []
                if self.current_token.type != 'RPAREN':
                    args.append(self.expr())
                    while self.current_token.type == 'COMMA':
                        self.eat('COMMA')
                        args.append(self.expr())
                self.eat('RPAREN')
                return FuncCall(id_name, args)
            else:
                return Var(id_name)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            self.error("Unexpected token in factor")
