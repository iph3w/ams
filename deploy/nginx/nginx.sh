#!/bin/bash

# cd /app/deploy/nginx

# sudo cp -rf app.conf /etc/nginx/sites-available/app
chmod 710 /app/web

sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "Started NGINX"

sudo systemctl status nginx