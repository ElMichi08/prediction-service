# Usamos una imagen base de Python
FROM python:3.10-slim

# Instalar Git
RUN apt-get update && apt-get install -y git

# Clonamos el repositorio de Git
RUN git clone https://github.com/ElMichi08/prediction-service.git

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para FastAPI
EXPOSE 8000
#Comandos aun pendientes

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
