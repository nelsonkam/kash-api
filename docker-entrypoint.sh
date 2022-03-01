#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
mkdir -p static/uploads
exec gunicorn --bind=0.0.0.0:5000 -w 6 app_main.wsgi:application --timeout 300
