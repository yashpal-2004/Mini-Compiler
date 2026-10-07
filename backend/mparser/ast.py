class ASTNode:
    def __init__(self, type_name):
        self.type = type_name

    def to_dict(self):
        return {"type": self.type}

class Program(ASTNode):
    def __init__(self, declarations):
        super().__init__("Program")
        self.declarations = declarations

    def to_dict(self):
        return {
            "type": self.type,
            "declarations": [d.to_dict() for d in self.declarations]
        }

class FunctionDeclaration(ASTNode):
    def __init__(self, return_type, name, body):
        super().__init__("FunctionDeclaration")
        self.return_type = return_type
        self.name = name
        self.body = body

    def to_dict(self):
        return {
            "type": self.type,
            "return_type": self.return_type,
            "name": self.name,
            "body": self.body.to_dict()
        }

class Block(ASTNode):
    def __init__(self, statements):
        super().__init__("Block")
        self.statements = statements

    def to_dict(self):
        return {
            "type": self.type,
            "statements": [s.to_dict() for s in self.statements]
        }

class VariableDeclaration(ASTNode):
    def __init__(self, var_type, name, initializer=None):
        super().__init__("VariableDeclaration")
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def to_dict(self):
        res = {
            "type": self.type,
            "var_type": self.var_type,
            "name": self.name
        }
        if self.initializer:
            res["initializer"] = self.initializer.to_dict()
        return res

class Assignment(ASTNode):
    def __init__(self, name, value):
        super().__init__("Assignment")
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "value": self.value.to_dict()
        }

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__("IfStatement")
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def to_dict(self):
        res = {
            "type": self.type,
            "condition": self.condition.to_dict(),
            "then_branch": self.then_branch.to_dict()
        }
        if self.else_branch:
            res["else_branch"] = self.else_branch.to_dict()
        return res

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        super().__init__("WhileStatement")
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": self.type,
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict()
        }

class ReturnStatement(ASTNode):
    def __init__(self, value):
        super().__init__("ReturnStatement")
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value.to_dict() if self.value else None
        }

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        super().__init__("BinaryExpression")
        self.left = left
        self.operator = operator
        self.right = right

    def to_dict(self):
        return {
            "type": self.type,
            "operator": self.operator,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }

class Literal(ASTNode):
    def __init__(self, value, literal_type):
        super().__init__("Literal")
        self.value = value
        self.literal_type = literal_type

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "literal_type": self.literal_type
        }

class Identifier(ASTNode):
    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name
        }
