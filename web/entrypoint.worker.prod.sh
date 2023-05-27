#!/bin/sh

until cd /home/app
do
    echo "Waiting for web volume..."
done

celery -A web worker --loglevel=info --concurrency 1 -E
