import copy

class Optimizer:
    def __init__(self, tac_instructions):
        self.original_tac = tac_instructions
        self.tac = [copy.deepcopy(t) for t in tac_instructions]
        self.optimizations = {
            "Constant Folding": 0,
            "Constant Propagation": 0,
            "Algebraic Simplification": 0,
            "Dead Code Elimination": 0
        }

    def optimize(self):
        changed = True
        iterations = 0
        while changed and iterations < 10:
            changed = False
            iterations += 1
            
            changed |= self.constant_folding()
            changed |= self.algebraic_simplification()
            changed |= self.constant_propagation()
            changed |= self.dead_code_elimination()

        opt_summary = []
        for name, count in self.optimizations.items():
            opt_summary.append({"name": name, "count": count})

        return self.tac, opt_summary

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
            
    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def constant_folding(self):
        changed = False
        for inst in self.tac:
            if inst.op in ['+', '-', '*', '/'] and self.is_number(inst.arg1) and self.is_number(inst.arg2):
                val1 = float(inst.arg1)
                val2 = float(inst.arg2)
                res = None
                
                if inst.op == '+': res = val1 + val2
                elif inst.op == '-': res = val1 - val2
                elif inst.op == '*': res = val1 * val2
                elif inst.op == '/': 
                    if val2 != 0: res = val1 / val2
                
                if res is not None:
                    if self.is_int(inst.arg1) and self.is_int(inst.arg2):
                        res = int(res)
                    inst.op = '='
                    inst.arg1 = str(res)
                    inst.arg2 = None
                    self.optimizations["Constant Folding"] += 1
                    changed = True
        return changed

    def algebraic_simplification(self):
        changed = False
        for inst in self.tac:
            if inst.op == '+' and inst.arg2 == '0':
                inst.op = '='
                inst.arg2 = None
                self.optimizations["Algebraic Simplification"] += 1
                changed = True
            elif inst.op == '+' and inst.arg1 == '0':
                inst.op = '='
                inst.arg1 = inst.arg2
                inst.arg2 = None
                self.optimizations["Algebraic Simplification"] += 1
                changed = True
            elif inst.op == '*' and inst.arg2 == '1':
                inst.op = '='
                inst.arg2 = None
                self.optimizations["Algebraic Simplification"] += 1
                changed = True
            elif inst.op == '*' and inst.arg1 == '1':
                inst.op = '='
                inst.arg1 = inst.arg2
                inst.arg2 = None
                self.optimizations["Algebraic Simplification"] += 1
                changed = True
            elif inst.op == '*' and (inst.arg1 == '0' or inst.arg2 == '0'):
                inst.op = '='
                inst.arg1 = '0'
                inst.arg2 = None
                self.optimizations["Algebraic Simplification"] += 1
                changed = True
        return changed

    def constant_propagation(self):
        changed = False
        constants = {}
        for inst in self.tac:
            if inst.op == '=' and self.is_number(inst.arg1):
                constants[inst.result] = inst.arg1
            
            if inst.arg1 in constants and inst.op != '=':
                inst.arg1 = constants[inst.arg1]
                self.optimizations["Constant Propagation"] += 1
                changed = True
            if inst.arg2 in constants:
                inst.arg2 = constants[inst.arg2]
                self.optimizations["Constant Propagation"] += 1
                changed = True
        return changed

    def dead_code_elimination(self):
        # A simple DCE that removes unused temporaries
        changed = False
        used = set()
        
        for inst in self.tac:
            if inst.arg1: used.add(inst.arg1)
            if inst.arg2: used.add(inst.arg2)
            if inst.op == 'ifFalse' or inst.op == 'return':
                if inst.arg1: used.add(inst.arg1)
                
        new_tac = []
        for inst in self.tac:
            # Keep labels, gotos, returns, ifFalse
            if inst.label or inst.op in ['goto', 'ifFalse', 'return']:
                new_tac.append(inst)
            elif inst.result and inst.result.startswith('t') and inst.result not in used:
                self.optimizations["Dead Code Elimination"] += 1
                changed = True
            else:
                new_tac.append(inst)
                
        self.tac = new_tac
        return changed
