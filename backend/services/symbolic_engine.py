# services/symbolic_engine.py
class SymbolicEngine:
    def __init__(self, expression, symbols):
        self.expression = expression
        self.symbols = symbols

    def evaluate(self, values: dict):
        return self.expression.subs(values).evalf()
