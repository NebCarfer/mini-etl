FROM python:3.11-slim

WORKDIR /app

COPY src/streaming/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/streaming /app/src/streaming
COPY src/common /app/src/common

ENV PYTHONPATH=/app/src

WORKDIR /app/src/streaming

# Ejecutar worker
CMD ["python", "processor.py"]