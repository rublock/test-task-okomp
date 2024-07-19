#!/bin/sh

set -e

whoami

#python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
#python app/load_cities.py

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi