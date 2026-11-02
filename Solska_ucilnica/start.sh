#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
if [ "${USTVARI_TESTNE_PODATKE:-1}" = "1" ]; then
  python manage.py seed
  python manage.py ustvari_admin
fi
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60
