from ast import *
from error import BrokenHandError

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise BrokenHandError(f"Variable '{name}' not defined")

    def set(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise BrokenHandError(f"Cannot assign to undefined variable '{name}'")

    def resolve(self, name):
        if name in self.vars:
            return True
        elif self.parent:
            return self.parent.resolve(name)
        else:
            return False

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.global_env = Environment()
        self.functions = {}

    def visit(self, node, env=None):
        if env is None:
            env = self.global_env
        method_name = 'visit_' + type(node).__name__
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, env)

    def no_visit_method(self, node, env):
        raise Exception(f"No visit_{type(node).__name__} method")

    def interpret(self):
        return self.visit(self.tree)

    def visit_Program(self, node, env):
        for stmt in node.statements:
            self.visit(stmt, env)

    def visit_Number(self, node, env):
        return node.value

    def visit_Boolean(self, node, env):
        return node.value

    def visit_Var(self, node, env):
        return env.get(node.name)

    def visit_Assign(self, node, env):
        value = self.visit(node.expr, env)
        if env.resolve(node.name):  # 如果變數已宣告過，就用 assign 更新
            env.assign(node.name, value)
        else:  # 如果沒宣告過，就用 set 新增
            env.set(node.name, value)

    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.op
        if op == 'PLUS':
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            else:
                raise BrokenHandError(
                    f"TypeError: unsupported operand types for +: '{type(left).__name__}' and '{type(right).__name__}'")
        elif op == 'MINUS':
            return left - right
        elif op == 'MUL':
            return left * right
        elif op == 'DIV':
            return left / right
        elif op == 'LT':
            return left < right
        elif op == 'GT':
            return left > right
        elif op == 'EQ':
            return left == right
        elif op == 'NE':
            return left != right
        elif op == 'LE':
            return left <= right
        elif op == 'GE':
            return left >= right
        elif op == 'AND':
            return left and right
        elif op == 'OR':
            return left or right
        else:
            raise BrokenHandError(f"Unknown binary operator {op}")

    def visit_Print(self, node, env):
        value = self.visit(node.expr, env)
        print(value)

    def visit_String(self, node, env):
        return node.value

    def visit_If(self, node, env):
        cond = self.visit(node.cond, env)
        if cond:
            for stmt in node.body:
                self.visit(stmt, env)
        elif node.else_body:
            for stmt in node.else_body:
                self.visit(stmt, env)

    def visit_While(self, node, env):
        while self.visit(node.cond, env):
            for stmt in node.body:
                self.visit(stmt, env)

    def visit_FunctionDef(self, node, env):
        env.set(node.name, node)

    def visit_FuncCall(self, node, env):
        try:
            func_def = env.get(node.name)
        except BrokenHandError:
            raise BrokenHandError(f"Function '{node.name}' is not defined")

        if len(func_def.params) != len(node.args):
            raise BrokenHandError(
                f"Function '{node.name}' expects {len(func_def.params)} arguments but got {len(node.args)}"
            )
        new_env = Environment(parent=self.global_env)
        for param, arg in zip(func_def.params, node.args):
            new_env.set(param, self.visit(arg, env))
        try:
            for stmt in func_def.body:
                self.visit(stmt, new_env)
        except ReturnValue as ret:
            return ret.value

    def visit_Return(self, node, env):
        value = self.visit(node.expr, env)
        raise ReturnValue(value)
