# services/uncertainty.py
from sympy import diff, sqrt

class UncertaintyAnalyzer:
    def __init__(self, expression, symbols):
        self.expression = expression
        self.symbols = symbols

    def propagate(self, uncertainties: dict):
        terms = []

        for symbol in self.symbols:
            sigma = uncertainties.get(str(symbol), 0)
            partial = diff(self.expression, symbol)
            terms.append((partial * sigma) ** 2)

        return sqrt(sum(terms))
