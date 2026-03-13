import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Gunicorn ishga tushganda avtomatik migrate + seed_data
from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=1)
    call_command('seed_data', verbosity=0)
except Exception as e:
    print(f"[wsgi] startup error: {e}")

application = get_wsgi_application()
