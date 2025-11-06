# Imagen base oficial de Python
FROM python:3.12-slim

# Evitar que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (ej. PostgreSQL client)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto: arrancar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
