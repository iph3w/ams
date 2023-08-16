#!/bin/bash

source env/bin/activate

cd /app/web

python3 manage.py migrate
echo "Database Migration Done."

python3 manage.py test
echo "Running Tests Done."

python3 manage.py collectstatic -- no-input
echo "Static Files Collected."

cd /app/deploy/gunicorn

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"

sudo systemctl daemon-reload
sudo systemctl start gunicorn

echo "Started Gunicorn."

sudo systemctl enable gunicorn

echo "Enabled Gunicorn."

sudo systemctl restart gunicorn

sudo systemctl status gunicorn
