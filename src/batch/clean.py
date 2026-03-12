from common.logger import get_logger

logger = get_logger("batch.clean")

def clean(records):
"""
Limpieza y validación de datos.
"""

cleaned = []

for r in records:
    try:
        value = int(r["value"])
        cleaned.append(value)
    except Exception:
        logger.warning(f"Invalid record skipped: {r}")

return cleaned