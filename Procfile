web: gunicorn app_main.wsgi:application --bind 0.0.0.0:${PORT:-8000}
release: python manage.py collectstatic --noinput