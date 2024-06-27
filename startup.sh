#!/bin/bash


echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Set the Python path to include your project root
export PYTHONPATH=$PYTHONPATH:/home/site/wwwroot/pg_RAG:/home/site/wwwroot/pg_RAG/RagApp
echo "PYTHONPATH: $PYTHONPATH"



# Navigate to the correct directory
cd /home/site/wwwroot/RagApp || exit
echo "Changed to directory: $(pwd)"


# List files in current directory
echo "Files in current directory:"
ls -la


# Start Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn --workers 3 --bind=0.0.0.0:8000 RagApp.wsgi:application
