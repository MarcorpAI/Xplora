#!/bin/bash


# <module-path> is the relative path to the folder that contains the module
# that contains wsgi.py; <module> is the name of the folder containing wsgi.py.
python manage.py makemigrations
python manage.py migrate
gunicorn --bind=0.0.0.0 --timeout 1200 --workers=4 --chdir RagApp RagApp.wsgi
