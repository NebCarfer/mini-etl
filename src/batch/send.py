import json
import os
from common.config import Config
from common.logger import get_logger

logger = get_logger("batch.send")

OUTPUT_FILE = os.path.join(Config.STAGING_PATH, "batch_output.jsonl")

def send(results):
    """
    Envía (persiste) los resultados.
    """

    os.makedirs(Config.STAGING_PATH, exist_ok=True)

    with open(OUTPUT_FILE, "a") as f:
        for r in results:
            f.write(json.dumps({"result": r}) + "\n")

    logger.info(f"Stored {len(results)} results")