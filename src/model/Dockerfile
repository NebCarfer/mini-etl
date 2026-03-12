FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código completo del modelo
COPY . .

# Exponer el puerto
EXPOSE 8000

# Ejecutar el servidor Flask
CMD ["python", "api.py"]