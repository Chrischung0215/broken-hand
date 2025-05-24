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
            raise NameError(f"Undefined variable: {name}")

    def set(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        """在已定義的地方更新變數，否則往上找，找不到就錯"""
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Cannot assign to undefined variable: {name}")
