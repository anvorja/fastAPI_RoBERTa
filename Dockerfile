FROM python:3.9-slim

WORKDIR /app

# Copiar solo los archivos necesarios primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8015

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8015", "--reload"]

