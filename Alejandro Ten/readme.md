cuando se  descarge entra  en la carpeta de  docker  y  haz docker compose up --build
y despues 
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser --noinput
