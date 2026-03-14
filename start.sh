#!/bin/bash
set -e
export PYTHONUNBUFFERED=1
echo "=== Creating directories ==="
mkdir -p media/murojaatlar media/tekshiruvlar staticfiles
echo "=== Running migrations ==="
python manage.py migrate --noinput --verbosity 1 2>&1
echo "=== Migrations done ==="
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --verbosity 1 2>&1
echo "=== Static done ==="
echo "=== Seeding data ==="
python manage.py seed_data 2>&1
echo "=== Seed done ==="
echo "=== Starting gunicorn ==="
exec python -m gunicorn core.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2
