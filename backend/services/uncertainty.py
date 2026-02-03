import sympy as sp

ALLOWED_CONSTANTS = {
    "pi": sp.pi,
    "e": sp.E,
    "E": sp.E,
    "inf": sp.oo,
    "oo": sp.oo
}

ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
    "sqrt": sp.sqrt,
    "abs": sp.Abs
}

class UncertaintyCalculator:
    def __init__(self, expression: str, variables: dict):
        # 1️⃣ Store raw inputs
        self.expression_str = expression
        self.variables = variables

        # 2️⃣ Create symbols ONLY for real variables
        self.symbols = {
            name: sp.Symbol(name) for name in variables.keys()
        }

        # 3️⃣ Parse expression with safe math context
        self.expression = sp.sympify(
            self.expression_str,
            locals={
                **self.symbols,
                **ALLOWED_CONSTANTS,
                **ALLOWED_FUNCTIONS
            }
        )

    def evaluate(self):
        subs = {
            self.symbols[name]: data["value"]
            for name, data in self.variables.items()
        }
        return float(self.expression.evalf(subs=subs))

    def propagate_uncertainty(self):
        variance = 0

        for name, data in self.variables.items():
            sigma = data["uncertainty"]
            symbol = self.symbols[name]

            partial = sp.diff(self.expression, symbol)
            partial_val = partial.evalf(subs={
                self.symbols[n]: v["value"]
                for n, v in self.variables.items()
            })

            variance += (partial_val * sigma) ** 2

        return float(sp.sqrt(variance))

    def symbolic_derivatives(self):
        return {
            name: str(sp.diff(self.expression, symbol))
            for name, symbol in self.symbols.items()
        }
