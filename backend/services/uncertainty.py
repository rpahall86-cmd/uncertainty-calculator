import sympy as sp

class UncertaintyCalculator:
    def __init__(self, expression: str, variables: dict, use_degrees: bool = False):
        self.expression_str = expression
        self.variables = variables
        self.use_degrees = use_degrees

        # 1️⃣ Create symbols (UNCHANGED)
        self.symbols = {
            name: sp.Symbol(name) for name in variables.keys()
        }

        # 2️⃣ Parse expression string → SymPy expression
        expr = sp.sympify(self.expression_str)

        # ======================================================
        # 🔥 THIS IS WHERE AUTO-NORMALIZATION GOES 🔥
        # ======================================================
        if self.use_degrees:
            trig_functions = (sp.sin, sp.cos, sp.tan)

            for func in trig_functions:
                expr = expr.replace(
                    lambda e: e.func == func,
                    lambda e: func(e.args[0] * sp.pi / 180)
                )
        # ======================================================
        # 🔥 END OF AUTO-NORMALIZATION 🔥
        # ======================================================

        # 3️⃣ Store the final normalized expression
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
