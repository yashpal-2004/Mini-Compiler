from semantic.symbol_table import SymbolTable, Symbol
from mparser.ast import *

class SemanticError(Exception):
    def __init__(self, message, suggestion=""):
        self.message = message
        self.suggestion = suggestion
        self.line = 0
        self.column = 0
        super().__init__(self.message)

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.warnings = []
        self.semantic_errors = []
        self.current_scope = "global"

    def analyze(self):
        self.visit(self.ast)

    def visit(self, node):
        if not node:
            return None
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.type} method')

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDeclaration(self, node):
        self.current_scope = node.name
        self.symbol_table.insert(Symbol(node.name, node.return_type, "global", True))
        self.visit(node.body)
        self.current_scope = "global"

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VariableDeclaration(self, node):
        if self.symbol_table.lookup(node.name, self.current_scope):
            raise SemanticError(f"Variable '{node.name}' is already declared in this scope.", "Rename the variable.")

        symbol = Symbol(node.name, node.var_type, self.current_scope, initialized=node.initializer is not None)
        self.symbol_table.insert(symbol)

        if node.initializer:
            init_type = self.visit(node.initializer)
            if not self.types_compatible(node.var_type, init_type):
                raise SemanticError(f"Cannot assign '{init_type}' to '{node.var_type}'.", "Ensure types match.")

    def visit_Assignment(self, node):
        symbol = self.symbol_table.lookup(node.name, self.current_scope)
        if not symbol:
            raise SemanticError(f"Variable '{node.name}' is not declared.", "Declare the variable before using it.")

        val_type = self.visit(node.value)
        if not self.types_compatible(symbol.type, val_type):
            raise SemanticError(f"Cannot assign '{val_type}' to '{symbol.type}'.", "Ensure types match.")

        symbol.initialized = True

    def visit_IfStatement(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise SemanticError(f"If condition must be a bool, got '{cond_type}'.", "Use comparison operators.")
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileStatement(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise SemanticError(f"While condition must be a bool, got '{cond_type}'.", "Use comparison operators.")

        # Detect obvious infinite loops
        self._check_infinite_loop(node)

        self.visit(node.body)

    def _check_infinite_loop(self, while_node):
        """
        Detect obvious infinite loop patterns:
        1. while (true) { ... }
        2. while (x > 0) { x = x + 1; } — condition variable is incremented, never decremented
        """
        cond = while_node.condition

        # Case 1: literal true
        if isinstance(cond, Literal) and cond.value is True:
            self.warnings.append({
                "message": "Possible infinite loop: condition is always true (while(true)).",
                "type": "infinite_loop"
            })
            return

        # Case 2: condition is BinaryExpression over a single variable
        # e.g. x > 0 or x < 10
        if isinstance(cond, BinaryExpression):
            loop_var = self._extract_loop_var(cond)
            if loop_var:
                direction = self._get_condition_direction(cond, loop_var)
                body_effect = self._get_body_effect(while_node.body, loop_var)

                # If condition says var should decrease (var > N) but body only increases it
                if direction == "must_decrease" and body_effect == "increases":
                    self.warnings.append({
                        "message": f"Possible infinite loop: '{loop_var}' increases but condition requires it to decrease.",
                        "type": "infinite_loop"
                    })
                # If condition says var should increase (var < N) but body only decreases it
                elif direction == "must_increase" and body_effect == "decreases":
                    self.warnings.append({
                        "message": f"Possible infinite loop: '{loop_var}' decreases but condition requires it to increase.",
                        "type": "infinite_loop"
                    })
                # If condition requires decrease and body increases
                elif direction == "must_decrease" and body_effect == "none":
                    self.warnings.append({
                        "message": f"Possible infinite loop: '{loop_var}' is never modified inside the loop.",
                        "type": "infinite_loop"
                    })
                elif direction == "must_increase" and body_effect == "none":
                    self.warnings.append({
                        "message": f"Possible infinite loop: '{loop_var}' is never modified inside the loop.",
                        "type": "infinite_loop"
                    })
                elif direction == "must_decrease" and body_effect == "unchanged":
                    pass  # loop will terminate
                elif direction == "must_decrease" and body_effect == "decreases":
                    self.warnings.append({
                        "message": f"Loop terminates: '{loop_var}' decreases toward the condition bound.",
                        "type": "loop_terminates"
                    })
                elif direction == "must_increase" and body_effect == "increases":
                    self.warnings.append({
                        "message": f"Loop terminates: '{loop_var}' increases toward the condition bound.",
                        "type": "loop_terminates"
                    })

    def _extract_loop_var(self, cond):
        """Return variable name if condition is of form: var op literal"""
        if isinstance(cond.left, Identifier) and isinstance(cond.right, Literal):
            return cond.left.name
        if isinstance(cond.right, Identifier) and isinstance(cond.left, Literal):
            return cond.right.name
        return None

    def _get_condition_direction(self, cond, var_name):
        """
        Determine what direction var must move for loop to terminate.
        Returns "must_decrease" or "must_increase" or "unknown"
        """
        op = cond.operator
        left_is_var = isinstance(cond.left, Identifier) and cond.left.name == var_name
        # var > N or var >= N → var must decrease to terminate
        if left_is_var and op in ['>', '>=']:
            return "must_decrease"
        # var < N or var <= N → var must increase to terminate
        if left_is_var and op in ['<', '<=']:
            return "must_increase"
        return "unknown"

    def _get_body_effect(self, body_node, var_name):
        """
        Check if var is increased or decreased inside the loop body.
        Returns "increases", "decreases", "none", or "unknown"
        """
        if isinstance(body_node, Block):
            for stmt in body_node.statements:
                effect = self._stmt_effect_on_var(stmt, var_name)
                if effect != "none":
                    return effect
            return "none"
        return "unknown"

    def _stmt_effect_on_var(self, stmt, var_name):
        """Check if a single statement increases/decreases the variable."""
        if isinstance(stmt, Assignment) and stmt.name == var_name:
            # e.g. x = x + 1 or x = x - 1
            if isinstance(stmt.value, BinaryExpression):
                expr = stmt.value
                is_self_ref = (isinstance(expr.left, Identifier) and expr.left.name == var_name)
                rhs_positive = isinstance(expr.right, Literal) and expr.right.value > 0
                if is_self_ref and expr.operator in ['+'] and rhs_positive:
                    return "increases"
                if is_self_ref and expr.operator in ['-'] and rhs_positive:
                    return "decreases"
        return "none"

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_BinaryExpression(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            if not (left_type in ['int', 'float'] and right_type in ['int', 'float']):
                raise SemanticError(f"Type mismatch: '{left_type}' and '{right_type}' with operator '{node.operator}'.")

        if node.operator in ['+', '-', '*', '/']:
            if left_type == 'bool' or right_type == 'bool':
                raise SemanticError("Arithmetic operations not allowed on bool.")
            return 'float' if left_type == 'float' or right_type == 'float' else 'int'
        elif node.operator in ['<', '>', '<=', '>=', '==', '!=']:
            return 'bool'
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                raise SemanticError("Logical operations require bool operands.")
            return 'bool'

        return left_type

    def visit_Identifier(self, node):
        symbol = self.symbol_table.lookup(node.name, self.current_scope)
        if not symbol:
            raise SemanticError(f"Variable '{node.name}' is not declared.", "Declare the variable before using it.")
        if not symbol.initialized:
            self.warnings.append({"message": f"Variable '{node.name}' might be used uninitialized."})
        return symbol.type

    def visit_Literal(self, node):
        return node.literal_type

    def types_compatible(self, target, source):
        if target == source:
            return True
        if target == "float" and source == "int":
            return True
        return False
