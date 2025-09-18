#!/usr/bin/env bash
set -e
python manage.py migrate --noinput || true

gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000 --workers 2
