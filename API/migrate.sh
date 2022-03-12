#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"astu@guide.com"}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"astu"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email "${SUPERUSER_EMAIL}" --username "${SUPERUSER_USERNAME}" --noinput || true