#!/bin/sh

# Exit on any error
set -e

echo "Starting Django application..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p /app/media/pdf_files
mkdir -p /app/media/converted_files
mkdir -p /app/staticfiles

# Set proper permissions for media directories
chmod 755 /app/media
chmod 755 /app/media/pdf_files
chmod 755 /app/media/converted_files

echo "Starting application..."

# Execute the main command
exec "$@"