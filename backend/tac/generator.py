class TACInstruction:
    def __init__(self, op, arg1=None, arg2=None, result=None, label=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        self.label = label

    def to_dict(self):
        return {
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "result": self.result,
            "label": self.label,
            "formatted": str(self)
        }

    def __str__(self):
        if self.label:
            return f"{self.label}:"
        
        if self.op == "goto":
            return f"goto {self.result}"
        elif self.op == "ifFalse":
            return f"ifFalse {self.arg1} goto {self.result}"
        elif self.op == "return":
            return f"return {self.arg1}" if self.arg1 else "return"
        elif self.op == "=":
            return f"{self.result} = {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class TACGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self):
        self.visit(self.ast)
        return self.instructions

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def add_instruction(self, inst):
        self.instructions.append(inst)

    def visit(self, node):
        if not node:
            return None
            
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'TAC: No visit_{node.type} method')

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDeclaration(self, node):
        self.add_instruction(TACInstruction(op=None, label=node.name))
        self.visit(node.body)

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VariableDeclaration(self, node):
        if node.initializer:
            val = self.visit(node.initializer)
            self.add_instruction(TACInstruction("=", arg1=val, result=node.name))

    def visit_Assignment(self, node):
        val = self.visit(node.value)
        self.add_instruction(TACInstruction("=", arg1=val, result=node.name))
        return node.name

    def visit_IfStatement(self, node):
        cond = self.visit(node.condition)
        label_false = self.new_label()
        label_end = self.new_label()
        
        self.add_instruction(TACInstruction("ifFalse", arg1=cond, result=label_false))
        self.visit(node.then_branch)
        
        if node.else_branch:
            self.add_instruction(TACInstruction("goto", result=label_end))
            self.add_instruction(TACInstruction(op=None, label=label_false))
            self.visit(node.else_branch)
            self.add_instruction(TACInstruction(op=None, label=label_end))
        else:
            self.add_instruction(TACInstruction(op=None, label=label_false))

    def visit_WhileStatement(self, node):
        label_start = self.new_label()
        label_end = self.new_label()
        
        self.add_instruction(TACInstruction(op=None, label=label_start))
        cond = self.visit(node.condition)
        self.add_instruction(TACInstruction("ifFalse", arg1=cond, result=label_end))
        
        self.visit(node.body)
        self.add_instruction(TACInstruction("goto", result=label_start))
        self.add_instruction(TACInstruction(op=None, label=label_end))

    def visit_ReturnStatement(self, node):
        val = None
        if node.value:
            val = self.visit(node.value)
        self.add_instruction(TACInstruction("return", arg1=val))

    def visit_BinaryExpression(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.add_instruction(TACInstruction(node.operator, arg1=left, arg2=right, result=temp))
        return temp

    def visit_Literal(self, node):
        if node.literal_type == "bool":
            return "true" if node.value else "false"
        return str(node.value)

    def visit_Identifier(self, node):
        return node.name
