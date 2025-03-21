# Imagen base de Python 3.12
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements-prod.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements-prod.txt

# Copiar código del proyecto
COPY . .

# Exponer puerto del backend
EXPOSE 4000

# Comando de inicio
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:4000"]
