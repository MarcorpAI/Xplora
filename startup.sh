#!/bin/bash

# Navigate to the directory containing manage.py
cd $(dirname "$0")

# Run migrations (optional, but often useful)
python manage.py migrate

# Start Gunicorn server
exec gunicorn --workers 3 --bind=0.0.0.0:8000 RagApp.RagApp.wsgi:application
