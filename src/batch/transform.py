import requests
from common.config import Config
from common.logger import get_logger

logger = get_logger("batch.transform")

def transform(values):
    """
    Llama al servicio del modelo para transformar datos.
    """

    results = []

    for v in values:
        response = requests.post(
            Config.MODEL_URL,
            json={"value": v}
        )

        if response.status_code == 200:
            result = response.json()["result"]
            results.append(result)
        else:
            logger.error(f"Model error for value {v}")

    return results