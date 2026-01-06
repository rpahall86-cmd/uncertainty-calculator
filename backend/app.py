# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.uncertainty import UncertaintyCalculator

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/calculate", methods=["POST"])
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

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
