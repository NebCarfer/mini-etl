FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/src/streaming
COPY ../common /app/src/common

WORKDIR /app/src/streaming

CMD ["python"]