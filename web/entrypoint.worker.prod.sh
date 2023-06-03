#!/bin/sh

until cd /home/app
do
    echo "Waiting for web volume..."
done

celery -A app worker -l INFO --concurrency 1 -E &

celery -A app beat -l info -S django &
