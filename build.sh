#!/usr/bin/env bash
#Exit on error
set -e errexit

#Modify this line as needed for your package manager
pip install -r requirements.txt

#Convert static assets files
python manage.py collectstatic --noinput

#Apply any outstanding database migrations
python manage.py migrate
