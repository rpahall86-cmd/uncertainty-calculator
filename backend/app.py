# app.py
from flask import Flask, request, jsonify
from models.expression_model import SymbolicExpression
from services.symbolic_engine import SymbolicEngine
from services.uncertainty import UncertaintyAnalyzer

class AnalysisAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule(
            "/analyze",
            view_func=self.analyze,
            methods=["POST"]
        )

    def analyze(self):
        data = request.json

        expr = SymbolicExpression(data["expression"])
        values = data["values"]
        uncertainties = data.get("uncertainties", {})

        engine = SymbolicEngine(expr.expression, expr.symbols)
        analyzer = UncertaintyAnalyzer(expr.expression, expr.symbols)

        result = engine.evaluate(values)
        uncertainty_expr = analyzer.propagate(uncertainties)
        uncertainty_value = uncertainty_expr.subs(values).evalf()

        return jsonify({
            "result": float(result),
            "uncertainty": float(uncertainty_value),
            "symbols": [str(s) for s in expr.symbols],
            "uncertainty_expression": str(uncertainty_expr)
        })

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    AnalysisAPI().run()
