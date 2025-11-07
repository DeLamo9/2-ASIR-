#!/bin/sh
set -e

# Espera a que MySQL esté listo
echo "⏳ Esperando a MySQL en $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ MySQL está listo."

# Ejecutar migraciones
echo "🏗️ Ejecutando migraciones..."
python manage.py migrate --noinput

# Crear superusuario automático si está configurado
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "👤 Creando superusuario..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username='$DJANGO_SUPERUSER_USERNAME';
email='$DJANGO_SUPERUSER_EMAIL';
password='$DJANGO_SUPERUSER_PASSWORD';
User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)
"
fi

# Collectstatic
echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "🚀 Iniciando Gunicorn..."
exec gunicorn hacienda.wsgi:application --bind 0.0.0.0:8000 --workers 3

