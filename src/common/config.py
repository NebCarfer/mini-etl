import os

class Config:
"""
Configuración centralizada del proyecto.
Todas las variables pueden sobrescribirse mediante variables de entorno.
"""

# modo de ejecución
MODE = os.getenv("MODE", "streaming")

# intervalo del batch (segundos)
BATCH_INTERVAL = int(os.getenv("BATCH_INTERVAL", 10))

# rutas de datos
STAGING_PATH = os.getenv("STAGING_PATH", "/app/src/staging")

# metadata
METADATA_PATH = os.getenv("METADATA_PATH", "/app/src/metadata")

# modelo
MODEL_URL = os.getenv("MODEL_URL", "http://model:8000/predict")