#!/bin/sh

# Exit on any error
set -e

echo "Starting Django application..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p /app/media/pdf_files
mkdir -p /app/staticfiles

echo "Starting application..."

# Execute the main command
exec "$@"