import json
import os
import time

from common.config import Config
from common.logger import get_logger

from clean import clean
from transform import transform
from send import send

logger = get_logger("batch.worker")

STAGING_FILE = os.path.join(Config.STAGING_PATH, "batch_input.jsonl")

def read_staging():
    if not os.path.exists(STAGING_FILE):
        return []

    records = []

    with open(STAGING_FILE) as f:
        for line in f:
            records.append(json.loads(line))

    open(STAGING_FILE, "w").close()

    return records

def run_batch_loop():
    logger.info("Batch worker started")

    while True:

        records = read_staging()

        if not records:
            logger.info("No records to process")
        else:
            logger.info(f"Processing batch of {len(records)} records")

            cleaned = clean(records)
            transformed = transform(cleaned)
            send(transformed)

        time.sleep(Config.BATCH_INTERVAL)


if __name__ == "__main__":
    run_batch_loop()