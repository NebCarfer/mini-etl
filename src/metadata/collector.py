import json
import os
import time
from common.config import Config
from common.logger import get_logger

logger = get_logger("metadata.collector")

METADATA_FILE = os.path.join(Config.METADATA_PATH, "metadata.jsonl")
os.makedirs(Config.METADATA_PATH, exist_ok=True)


def log_metadata(input_value, output_value, status="ok"):
    """
    Registra metadatos de cada ejecución.
    """
    record = {
        "timestamp": time.time(),
        "input": input_value,
        "output": output_value,
        "status": status
    }

    with open(METADATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    logger.info(f"Metadata logged for input {input_value}")