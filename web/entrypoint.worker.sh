#!/bin/sh

until cd /usr/src/app/
do
    echo "Waiting for web volume..."
done

celery -A app worker -l INFO --concurrency 1 -E &

exec "$@"
