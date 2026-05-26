#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --log-file - \
    --access-logfile - \
    --error-logfile - \
    --log-level info
