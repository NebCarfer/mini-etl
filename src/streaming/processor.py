from flask import Flask, request, jsonify
import requests
from common.config import Config
from common.logger import get_logger

logger = get_logger("streaming.processor")

app = Flask(__name__)

def process(value: int):
    try:
        value = int(value)
    except ValueError:
        raise ValueError("Input must be an integer")

    response = requests.post(
        Config.MODEL_URL,
        json={"value": value}
    )

    if response.status_code != 200:
        raise RuntimeError("Model service error")

    result = response.json()["result"]

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