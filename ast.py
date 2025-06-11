class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Number(Node):
    def __init__(self, value):
        self.value = value

class Boolean(Node):
    def __init__(self, value):
        self.value = value

class Var(Node):
    def __init__(self, name):
        self.name = name

class Assign(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

class If(Node):
    def __init__(self, cond, body, else_body=None):
        self.cond = cond
        self.body = body
        self.else_body = else_body

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Node):
    def __init__(self, init, cond, update, body):
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body

class FunctionDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FuncCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return(Node):
    def __init__(self, expr):
        self.expr = expr
class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
class String(Node):
    def __init__(self, value):
        self.value = value
class Switch(Node):
    def __init__(self, expr, cases, default=None):
        self.expr = expr
        self.cases = cases
        self.default = default
class Break(Node):
    pass

class Continue(Node):
    pass