# src/batch/send.py
import json
import os
from common.config import Config
from common.logger import get_logger

logger = get_logger("batch.send")

# Archivo en staging (opcional, puedes seguir manteniéndolo)
OUTPUT_FILE = os.path.join(Config.STAGING_PATH, "batch_output.jsonl")

# Archivo para metadata que lee el frontend
RESULTS_FILE = os.path.join(Config.METADATA_PATH, "batch_results.jsonl")

def send(results, inputs=None):
    """
    Envía (persiste) los resultados tanto a staging como a metadata.
    `results` es la lista de valores transformados.
    `inputs` es opcional, lista de valores originales para mantener input/output.
    """
    os.makedirs(Config.STAGING_PATH, exist_ok=True)
    os.makedirs(Config.METADATA_PATH, exist_ok=True)

    # Guardar en staging (como antes)
    with open(OUTPUT_FILE, "a") as f:
        for r in results:
            f.write(json.dumps({"result": r}) + "\n")

    # Guardar en metadata con input/output para frontend
    with open(RESULTS_FILE, "a") as f:
        for i, r in enumerate(results):
            input_val = inputs[i] if inputs else None
            f.write(json.dumps({"input": input_val, "output": r}) + "\n")

    logger.info(f"Stored {len(results)} results")