from flask import Flask, request, jsonify
from model import predict  # Asegúrate de que predict está en model/__init__.py

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json

    if "value" not in data:
        return jsonify({"error": "Missing 'value'"}), 400

    try:
        x = int(data["value"])
    except ValueError:
        return jsonify({"error": "Value must be an integer"}), 400

    result = predict(x)
    return jsonify({"result": result})

# Esto es clave: mantiene el contenedor vivo
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)