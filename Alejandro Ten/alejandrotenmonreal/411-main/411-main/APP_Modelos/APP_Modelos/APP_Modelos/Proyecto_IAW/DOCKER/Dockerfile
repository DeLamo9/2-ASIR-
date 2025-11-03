# Imagen base
FROM python:3.11-slim

# Evita .pyc y habilita logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Paquetes necesarios para compilar psycopg2 y libpq
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Instala requirements de tu carpeta DOCKER
COPY DOCKER/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo el proyecto (manage.py está en la raíz del contexto)
COPY . /app

# Expone el puerto de Django
EXPOSE 8000

# Comando: migra y arranca el servidor
# (el healthcheck del servicio db en docker-compose garantiza que ya está listo)
CMD [ "sh", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000" ]
