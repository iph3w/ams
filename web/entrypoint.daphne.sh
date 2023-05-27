#!/bin/sh

until cd /usr/src/app/
do
    echo "Waiting for web volume..."
done

# daphne app.asgi:application &

exec "$@"
