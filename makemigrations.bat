@ECHO OFF

ECHO MAKE MIGRATIONS

docker-compose run web python manage.py makemigrations

ECHO MIGRATE

docker-compose run web python manage.py migrate

PAUSE