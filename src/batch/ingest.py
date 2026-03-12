import json
import os
import time
from common.config import Config
from common.logger import get_logger

logger = get_logger("batch.ingest")

STAGING_FILE = os.path.join(Config.STAGING_PATH, "batch_input.jsonl")

def ingest(value: int):
"""
Extrae el dato recibido del frontend
y lo guarda en staging.
"""

os.makedirs(Config.STAGING_PATH, exist_ok=True)

record = {
    "value": value,
    "timestamp": time.time()
}

with open(STAGING_FILE, "a") as f:
    f.write(json.dumps(record) + "\n")

logger.info(f"Value stored in staging: {value}")