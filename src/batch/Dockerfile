FROM python:3.11-slim
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY src/batch/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

WORKDIR /app/src/batch

CMD ["python", "worker.py"]