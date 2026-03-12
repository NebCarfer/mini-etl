from flask import Flask, request, jsonify
from model import predict

app = Flask(name)

@app.route("/predict", methods=["POST"])
def predict_endpoint():
"""
Endpoint HTTP para acceder al modelo.
"""

data = request.json

if "value" not in data:
    return jsonify({"error": "Missing 'value'"}), 400

try:
    x = int(data["value"])
except ValueError:
    return jsonify({"error": "Value must be an integer"}), 400

result = predict(x)

return jsonify({"result": result})