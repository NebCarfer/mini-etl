FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/src/batch
COPY ../common /app/src/common

WORKDIR /app/src/batch

CMD ["python", "worker.py"]