#!/bin/sh

flask db upgrade
exec gunicorn --bind=0.0.0.0:5000 "app:create_app()" -w 2
