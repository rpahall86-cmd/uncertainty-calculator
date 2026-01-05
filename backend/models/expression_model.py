# models/expression_model.py
from sympy import symbols, sympify

class SymbolicExpression:
    def __init__(self, expression_str: str):
        self.expression_str = expression_str
        self.symbols = self._extract_symbols()
        self.expression = sympify(expression_str)

    def _extract_symbols(self):
        return sorted(
            list(sympify(self.expression_str).free_symbols),
            key=lambda s: s.name
        )

