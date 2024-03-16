#! /bin/bash
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
