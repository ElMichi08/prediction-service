# Usamos una imagen base de Python
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    python3-dev \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Clonar repositorio directamente en /app
RUN git clone https://github.com/ElMichi08/prediction-service.git /app

# Copiar el archivo data.csv al contenedor si es necesario
COPY ./data.csv /app/data.csv

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    scikit-learn \
    pandas \
    numpy \
    joblib

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
