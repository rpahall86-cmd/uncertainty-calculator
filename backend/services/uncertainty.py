import sympy as sp

class UncertaintyCalculator:
    def __init__(self, expression: str, variables: dict):
        """
        expression: string, e.g. "x*y + z"
        variables: {
            "x": {"value": 2.0, "uncertainty": 0.1},
            "y": {"value": 3.0, "uncertainty": 0.2}
        }
        """
        self.expression_str = expression
        self.variables = variables

        self.symbols = {
            name: sp.Symbol(name) for name in variables.keys()
        }

        self.expression = sp.sympify(self.expression_str)

    def evaluate(self):
        """Evaluate the expression numerically."""
        subs = {
            self.symbols[name]: data["value"]
            for name, data in self.variables.items()
        }
        return float(self.expression.evalf(subs=subs))

    def propagate_uncertainty(self):
        """Compute propagated uncertainty using partial derivatives."""
        variance = 0

        for name, data in self.variables.items():
            symbol = self.symbols[name]
            sigma = data["uncertainty"]

            partial = sp.diff(self.expression, symbol)
            partial_val = partial.evalf(subs={
                self.symbols[n]: v["value"]
                for n, v in self.variables.items()
            })

            variance += (partial_val * sigma) ** 2

        return float(sp.sqrt(variance))

    def symbolic_derivatives(self):
        """Return symbolic partial derivatives."""
        return {
            name: str(sp.diff(self.expression, symbol))
            for name, symbol in self.symbols.items()
        }
