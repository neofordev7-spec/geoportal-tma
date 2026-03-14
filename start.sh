#!/bin/bash
set -e
echo "=== Creating directories ==="
mkdir -p media/murojaatlar media/tekshiruvlar staticfiles
echo "=== Running migrations ==="
python manage.py migrate --noinput
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput
echo "=== Seeding data ==="
python manage.py seed_data
echo "=== Starting gunicorn ==="
exec python -m gunicorn core.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2
