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

    # URLs
    MODEL_URL = os.getenv("MODEL_URL", "http://model:8000/predict")
    BATCH_URL = os.getenv("BATCH_URL", "http://batch-worker:5000/submit")
    STREAMING_URL = os.getenv("STREAMING_URL", "http://streaming-worker:5001/submit")