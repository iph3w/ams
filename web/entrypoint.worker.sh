#!/bin/sh

until cd /usr/src/app/
do
    echo "Waiting for web volume..."
done

celery -A app beat -l info -S django &

exec "$@"
