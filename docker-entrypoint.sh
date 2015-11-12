#!/bin/bash
python manage.py syncdb                   # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/access.log
tail -n 0 -f /logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn imio_geonode.wsgi:application \
    --name imio_geonode \
    --bind 0.0.0.0:8000 \
    --workers 8 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/access.log \
    "$@"
