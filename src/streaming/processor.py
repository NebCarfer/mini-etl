import requests
from common.config import Config
from common.logger import get_logger

logger = get_logger("streaming.processor")

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