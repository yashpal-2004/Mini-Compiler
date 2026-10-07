class Symbol:
    def __init__(self, name, type_val, scope, initialized=False):
        self.name = name
        self.type = type_val
        self.scope = scope
        self.initialized = initialized

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "scope": self.scope,
            "initialized": self.initialized
        }

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, symbol):
        key = f"{symbol.scope}_{symbol.name}"
        self.symbols[key] = symbol

    def lookup(self, name, scope):
        key = f"{scope}_{name}"
        return self.symbols.get(key)
        
    def get_all(self):
        return [s.to_dict() for s in self.symbols.values()]
