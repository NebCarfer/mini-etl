FROM python:3.11-slim

WORKDIR /app

COPY src/frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/frontend /app/src/frontend
COPY src/common /app/src/common

WORKDIR /app/src/frontend

EXPOSE 1936

CMD ["python", "app.py"]