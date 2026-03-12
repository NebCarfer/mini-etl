FROM python:3.11-slim

ENV PYTHONPATH=/app/src

WORKDIR /app/src

COPY src/frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/frontend /app/src/frontend
COPY src/common /app/src/common

EXPOSE 1936

# Ejecutar frontend como módulo
CMD ["python", "-m", "frontend.app"]