import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Django setup
django.setup()

# Migrate + seed — gunicorn ishga tushganda
from django.core.management import call_command
try:
    call_command('migrate', '--noinput', verbosity=1)
    print("[wsgi] Migrate done")
except Exception as e:
    print(f"[wsgi] Migrate error: {e}")

try:
    call_command('seed_data', verbosity=1)
    print("[wsgi] Seed done")
except Exception as e:
    print(f"[wsgi] Seed error: {e}")

application = get_wsgi_application()
