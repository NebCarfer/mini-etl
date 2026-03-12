# src/frontend/app.py
from flask import Flask, request, render_template, redirect, url_for
import requests
from common.config import Config
from common.logger import get_logger
import os
import json

logger = get_logger("frontend.app")

app = Flask(__name__, template_folder="templates", static_folder="static")

STAGING_FILE = "/app/src/staging/batch_input.jsonl"
RESULTS_FILE = "/app/src/metadata/batch_results.jsonl"


def read_batch_results():
    """
    Lee los resultados procesados por el batch worker.
    """
    if not os.path.exists(RESULTS_FILE):
        return []

    results = []

    try:
        with open(RESULTS_FILE) as f:
            for line in f:
                results.append(json.loads(line))
    except Exception as e:
        logger.error(f"Error leyendo metadata: {e}")

    return results


@app.route("/", methods=["GET"])
def index():
    results = read_batch_results()
    return render_template(
        "index.html",
        input_value=None,
        output_value=None,
        error=None,
        results=results
    )


@app.route("/submit", methods=["POST"])
def submit():
    value = request.form.get("number")

    if not value:
        return render_template(
            "index.html",
            input_value=None,
            output_value=None,
            error="Por favor ingresa un número",
            results=read_batch_results()
        ), 400

    try:
        x = int(value)
    except ValueError:
        return render_template(
            "index.html",
            input_value=value,
            output_value=None,
            error="Debe ser un número entero",
            results=read_batch_results()
        ), 400

    try:
        if Config.MODE == "batch":
            os.makedirs(os.path.dirname(STAGING_FILE), exist_ok=True)
            with open(STAGING_FILE, "a") as f:
                f.write(json.dumps({"value": x}) + "\n")
            result = "Encolado para batch"

        elif Config.MODE == "streaming":
            response = requests.post(Config.STREAMING_URL, json={"value": x})
            response.raise_for_status()
            result = response.json()["result"]

        else:
            raise ValueError("mode must be batch or streaming (edit in .env)")

    except Exception as e:
        logger.error(f"Error procesando número: {e}")
        return render_template(
            "index.html",
            input_value=x,
            output_value=None,
            error=f"Error: {e}",
            results=read_batch_results()
        ), 500

    return render_template(
        "index.html",
        input_value=x,
        output_value=result,
        error=None,
        results=read_batch_results()
    )


# Redirigir cualquier GET a /submit hacia /
@app.route("/submit", methods=["GET"])
def submit_get():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1936, debug=True)