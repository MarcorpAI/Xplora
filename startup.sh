#!/bin/bash

# Navigate to the directory containing manage.py
cd RagApp

# Run migrations (optional, but often useful)
python RagApp/manage.py migrate

# Start Gunicorn server
exec gunicorn --workers 3 --bind=0.0.0.0:8000 RagApp.wsgi:application
