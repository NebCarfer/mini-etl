FROM python:3.11-slim

WORKDIR /app

COPY src/batch/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/batch /app/src/batch
COPY src/common /app/src/common

WORKDIR /app/src/batch

CMD ["python", "worker.py"]