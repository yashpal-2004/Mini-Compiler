class CodeGenerator:
    def __init__(self, tac_instructions):
        self.tac = tac_instructions
        self.assembly = []
        self.reg_count = 0
        self.var_to_reg = {}

    def get_reg(self, var):
        if var in self.var_to_reg:
            return self.var_to_reg[var]
        
        self.reg_count = (self.reg_count % 8) + 1
        reg = f"R{self.reg_count}"
        self.var_to_reg[var] = reg
        return reg

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def generate(self):
        for inst in self.tac:
            if inst.label:
                self.assembly.append(f"{inst.label}:")
                continue
                
            if inst.op == "=":
                reg = self.get_reg(inst.result)
                if self.is_number(inst.arg1) or inst.arg1 in ['true', 'false']:
                    self.assembly.append(f"LOADI {reg}, {inst.arg1}")
                else:
                    arg_reg = self.get_reg(inst.arg1)
                    if arg_reg != reg:
                        self.assembly.append(f"LOAD {reg}, {inst.arg1}")
                self.assembly.append(f"STORE {inst.result}, {reg}")
                
            elif inst.op in ['+', '-', '*', '/']:
                reg1 = self.get_reg(inst.arg1)
                
                if not self.is_number(inst.arg1):
                    self.assembly.append(f"LOAD {reg1}, {inst.arg1}")
                else:
                    self.assembly.append(f"LOADI {reg1}, {inst.arg1}")

                if self.is_number(inst.arg2):
                    reg2 = self.get_reg(f"const_{inst.arg2}")
                    self.assembly.append(f"LOADI {reg2}, {inst.arg2}")
                else:
                    reg2 = self.get_reg(inst.arg2)
                    self.assembly.append(f"LOAD {reg2}, {inst.arg2}")

                op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
                asm_op = op_map[inst.op]
                
                self.assembly.append(f"{asm_op} {reg1}, {reg2}")
                self.assembly.append(f"STORE {inst.result}, {reg1}")

            elif inst.op in ['<', '>', '<=', '>=', '==', '!=']:
                reg1 = self.get_reg(inst.arg1)
                if not self.is_number(inst.arg1):
                    self.assembly.append(f"LOAD {reg1}, {inst.arg1}")
                else:
                    self.assembly.append(f"LOADI {reg1}, {inst.arg1}")

                if self.is_number(inst.arg2):
                    self.assembly.append(f"CMP {reg1}, {inst.arg2}")
                else:
                    reg2 = self.get_reg(inst.arg2)
                    self.assembly.append(f"LOAD {reg2}, {inst.arg2}")
                    self.assembly.append(f"CMP {reg1}, {reg2}")

                # Storing result of comparison in a temporary register (simplified)
                res_reg = self.get_reg(inst.result)
                op_map = {'<': 'SETL', '>': 'SETG', '<=': 'SETLE', '>=': 'SETGE', '==': 'SETE', '!=': 'SETNE'}
                self.assembly.append(f"{op_map[inst.op]} {res_reg}")
                self.assembly.append(f"STORE {inst.result}, {res_reg}")

            elif inst.op == "ifFalse":
                reg = self.get_reg(inst.arg1)
                self.assembly.append(f"LOAD {reg}, {inst.arg1}")
                self.assembly.append(f"CMP {reg}, 0")
                self.assembly.append(f"JEQ {inst.result}")

            elif inst.op == "goto":
                self.assembly.append(f"JMP {inst.result}")

            elif inst.op == "return":
                if inst.arg1:
                    reg = self.get_reg(inst.arg1)
                    if not self.is_number(inst.arg1):
                        self.assembly.append(f"LOAD {reg}, {inst.arg1}")
                    else:
                        self.assembly.append(f"LOADI {reg}, {inst.arg1}")
                    self.assembly.append(f"RET {reg}")
                else:
                    self.assembly.append("RET")

        return self.assembly
