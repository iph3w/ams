#!/bin/bash

sudo apt update
sudo apt install gcc python3 python3-venv python3-dev python3-pip libpq-dev postgresql-dev nginx curl musl-dev redis-server

mkdir ~/myprojectdir
cd ~/myprojectdir

pip3 install virtualenv

mkdir /logs
touch /logs/error.log /logs/access.log
chmod -R 777 /logs

if [ -d "env" ]
then
    echo "Python virtual Environment Exists."
else
    python3 -m venv env
fi

source env/bin/activate
pip3 install --upgrade pip3

pip3 install -r requirements.txt
pip3 install channels["daphne"]
