#!/bin/sh

python db.py migrate -f -n
exec gunicorn --bind=0.0.0.0:5000 "app:create_app()" -w 2
