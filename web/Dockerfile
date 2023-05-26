FROM python:3.11.3-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/ams
RUN mkdir -p /log
COPY . /app/ams
WORKDIR /app/ams

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

RUN apk add netcat-openbsd

RUN pip install --upgrade pip
RUN pip install -r requirements.dev.txt
RUN pip install channels["daphne"]