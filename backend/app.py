from flask import Flask, request, jsonify
from flask_cors import CORS
from services.uncertainty import UncertaintyCalculator

app = Flask(__name__)
CORS(app)

# Health check (GET /)
@app.route("/", methods=["GET"])
def health():
    return {"status": "running"}

# Main calculation endpoint (POST /calculate)
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    calculator = UncertaintyCalculator(
        expression=data["expression"],
        variables=data["variables"]
    )

    return jsonify({
        "expression": data["expression"],
        "value": calculator.evaluate(),
        "uncertainty": calculator.propagate_uncertainty(),
        "partials": calculator.symbolic_derivatives()
    })
