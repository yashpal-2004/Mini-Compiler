"""
Safe static interpreter for MiniLang.
Does NOT execute arbitrary code. Performs static control-flow analysis only.
"""
from mparser.ast import *


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.env = {}          # variable -> value (when known statically)
        self.analysis = []     # list of analysis result dicts

    def run(self):
        self._visit(self.ast)
        return self.analysis

    def _visit(self, node):
        if node is None:
            return None
        method = f'_visit_{node.type}'
        return getattr(self, method, self._noop)(node)

    def _noop(self, node):
        return None

    def _visit_Program(self, node):
        for decl in node.declarations:
            self._visit(decl)

    def _visit_FunctionDeclaration(self, node):
        self.analysis.append({
            "type": "info",
            "message": f"Entering function '{node.name}' (return type: {node.return_type})"
        })
        self._visit(node.body)

    def _visit_Block(self, node):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VariableDeclaration(self, node):
        if node.initializer:
            val = self._eval(node.initializer)
            self.env[node.name] = val
            self.analysis.append({
                "type": "info",
                "message": f"Variable '{node.name}' declared as {node.var_type} = {val}"
            })
        else:
            self.env[node.name] = None
            self.analysis.append({
                "type": "info",
                "message": f"Variable '{node.name}' declared as {node.var_type} (uninitialized)"
            })

    def _visit_Assignment(self, node):
        val = self._eval(node.value)
        self.env[node.name] = val
        self.analysis.append({
            "type": "info",
            "message": f"'{node.name}' assigned value: {val if val is not None else '(unknown)'}"
        })

    def _visit_IfStatement(self, node):
        cond_val = self._eval(node.condition)
        if cond_val is True:
            self.analysis.append({"type": "info", "message": "If condition is always true (statically known)."})
            self._visit(node.then_branch)
        elif cond_val is False:
            self.analysis.append({"type": "warning", "message": "If condition is always false — then-branch is unreachable."})
            if node.else_branch:
                self._visit(node.else_branch)
        else:
            self.analysis.append({"type": "info", "message": "If condition depends on runtime values."})
            self._visit(node.then_branch)
            if node.else_branch:
                self._visit(node.else_branch)

    def _visit_WhileStatement(self, node):
        cond_val = self._eval(node.condition)
        if cond_val is True:
            self.analysis.append({
                "type": "warning",
                "message": "While condition is always true — possible infinite loop."
            })
        elif cond_val is False:
            self.analysis.append({
                "type": "warning",
                "message": "While condition is always false — loop body is unreachable."
            })
        else:
            self.analysis.append({
                "type": "info",
                "message": "While loop depends on runtime values."
            })
        # Do not recurse body to avoid false infinite execution

    def _visit_ReturnStatement(self, node):
        val = self._eval(node.value) if node.value else None
        self.analysis.append({
            "type": "info",
            "message": f"Return value: {val if val is not None else '(unknown)'}"
        })

    def _eval(self, node):
        """Evaluate an expression statically, returning a Python value or None."""
        if node is None:
            return None
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Identifier):
            return self.env.get(node.name)  # None if unknown
        if isinstance(node, BinaryExpression):
            l = self._eval(node.left)
            r = self._eval(node.right)
            if l is None or r is None:
                return None
            try:
                ops = {
                    '+': lambda a, b: a + b,
                    '-': lambda a, b: a - b,
                    '*': lambda a, b: a * b,
                    '/': lambda a, b: a / b if b != 0 else None,
                    '>': lambda a, b: a > b,
                    '<': lambda a, b: a < b,
                    '>=': lambda a, b: a >= b,
                    '<=': lambda a, b: a <= b,
                    '==': lambda a, b: a == b,
                    '!=': lambda a, b: a != b,
                    '&&': lambda a, b: a and b,
                    '||': lambda a, b: a or b,
                }
                return ops[node.operator](l, r)
            except Exception:
                return None
        return None
