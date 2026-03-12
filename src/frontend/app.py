from flask import Flask, request, render_template, jsonify
import requests
from common.config import Config
from common.logger import get_logger

logger = get_logger("frontend.app")

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    value = request.form.get("number")

    if not value:
        return "Por favor ingresa un número", 400

    try:
        x = int(value)
    except ValueError:
        return "Debe ser un número entero", 400

    # Llama al modelo directamente vía API
    response = requests.post(Config.MODEL_URL, json={"value": x})

    if response.status_code != 200:
        return f"Error en el modelo: {response.text}", 500

    result = response.json()["result"]
    return render_template("index.html", input_value=x, output_value=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1936)