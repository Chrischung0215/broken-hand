﻿class Environment:
    def __init__(self):
        self.vars = {}

    def get(self, name):
        if name not in self.vars:
            raise NameError(f"Undefined variable: {name}")
        return self.vars[name]

    def set(self, name, value):
        self.vars[name] = value
