
1. Crear la base de datos vacía dentro de un contenedor PostgreSQL:

docker exec -it postgres_IVA psql -U postgres -c "CREATE DATABASE tienda_db;"


2. Importar el archivo .sql que esta en el zip:

docker exec -i postgres_IVA psql -U postgres -d tienda_db < tienda_db_backup.sql
