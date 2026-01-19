import sympy as sp

class UncertaintyCalculator:
    def __init__(self, expression: str, variables: dict, use_degrees: bool = False):
        """
        expression: string, e.g. "x*y + z" or "sin(x)"
        variables: {
            "x": {"value": 2.0, "uncertainty": 0.1},
            "y": {"value": 3.0, "uncertainty": 0.2}
        }
        use_degrees: bool (convert trig inputs from degrees to radians)
        """
        self.expression_str = expression
        self.variables = variables
        self.use_degrees = use_degrees

        # Create symbols
        self.symbols = {
            name: sp.Symbol(name) for name in variables.keys()
        }

        # Parse expression
        expr = sp.sympify(self.expression_str)

        # Convert degrees → radians if requested
        if self.use_degrees:
            for name, symbol in self.symbols.items():
                expr = expr.subs(symbol, symbol * sp.pi / 180)

        self.expression = expr

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

        subs = {
            self.symbols[name]: data["value"]
            for name, data in self.variables.items()
        }

        for name, data in self.variables.items():
            symbol = self.symbols[name]
            sigma = data["uncertainty"]

            partial = sp.diff(self.expression, symbol)
            partial_val = partial.evalf(subs=subs)

            variance += (partial_val * sigma) ** 2

        return float(sp.sqrt(variance))

    def symbolic_derivatives(self):
        """Return symbolic partial derivatives."""
        return {
            name: str(sp.diff(self.expression, symbol))
            for name, symbol in self.symbols.items()
        }
