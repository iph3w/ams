#!/bin/sh

until cd /usr/src/app/
do
    echo "Waiting for web volume..."
done

python manage.py makemigrations

python manage.py migrate

flake8 --ignore=E501,W293

python manage.py test

exec "$@"