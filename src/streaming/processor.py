from flask import Flask, request, jsonify
import requests
from common.config import Config
from common.logger import get_logger
import os
import json

logger = get_logger("streaming.processor")
RESULTS_FILE = os.path.join(Config.METADATA_PATH, "batch_results.jsonl")

app = Flask(__name__)

def process(value: int):
    try:
        value = int(value)
    except ValueError:
        raise ValueError("Input must be an integer")

    # Llamada al modelo
    response = requests.post(Config.MODEL_URL, json={"value": value})
    if response.status_code != 200:
        raise RuntimeError("Model service error")

    result = response.json()["result"]

    # Guardar metadata del streaming
    os.makedirs(Config.METADATA_PATH, exist_ok=True)
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps({"input": value, "output": result}) + "\n")

    logger.info(f"Processed streaming value {value} -> {result}")
    return result

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if "value" not in data:
        return jsonify({"error": "Missing 'value'"}), 400

    try:
        result = process(data["value"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)