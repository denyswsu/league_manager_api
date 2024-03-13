#! /bin/bash
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
#python3 manage.py runserver 0.0.0.0:8000
# Here we are using gunicorn with hot reload here to simplify development,
# of course you won't do this in production.
exec gunicorn  config.wsgi -b 0.0.0.0:8000 --reload --timeout 120 --workers 2
