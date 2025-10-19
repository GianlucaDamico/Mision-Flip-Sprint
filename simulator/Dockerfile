# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos todos los archivos del simulador al contenedor
COPY . /app

# Instalamos dependencias si tenés un requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found, skipping"

# Comando por defecto para ejecutar el simulador
CMD ["python", "simulator.py", "--parcel", "BX-001", "--seconds", "3600"]
