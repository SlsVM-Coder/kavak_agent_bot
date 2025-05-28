# Dockerfile

# 1) Imagen base con Python 3.13-slim (sin vulnerabilidades críticas)
FROM python:3.13-slim

# 2) Variables para no generar .pyc y deshabilitar cache de pip
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3) Directorio de trabajo
WORKDIR /app

# 4) Copiamos únicamente requirements.txt para cachear instalación
COPY requirements.txt .

# 5) Instalamos dependencias
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 6) Copiamos el resto del código
COPY . .

# 7) Exponemos el puerto
EXPOSE 8000

# 8) Punto de entrada
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
