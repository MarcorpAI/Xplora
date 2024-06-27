#!/bin/bash

# Set the Python path to include your project root
export PYTHONPATH=$PYTHONPATH:/home/site/wwwroot/pg_RAG:/home/site/wwwroot/pg_RAG/RagApp


# Run migrations (optional, but often useful)
cd /home/site/wwwroot/RagApp/RagApp


# Start Gunicorn server
exec gunicorn --workers 3 --bind=0.0.0.0:8000 RagApp.wsgi:application
