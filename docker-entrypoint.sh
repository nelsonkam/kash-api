#!/bin/sh

python manage.py migrate
exec gunicorn --bind=0.0.0.0:5000 -w 6 kweek_api.wsgi:application --timeout 300
