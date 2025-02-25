#!/bin/sh

set -e

whoami

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata dumped_data.json

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi