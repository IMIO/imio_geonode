#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /var/logs/gunicorn.log
touch /var/logs/access.log
tail -n 0 -f /var/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn imio_geonode.wsgi:application \
    --name imio_geonode \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/var/logs/gunicorn.log \
    --access-logfile=/var/logs/access.log \
    "$@"
