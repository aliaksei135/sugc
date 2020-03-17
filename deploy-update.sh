#!/bin/sh
# Simple updating script from git
git pull
source ../venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
sudo systemctl restart gunicorn

