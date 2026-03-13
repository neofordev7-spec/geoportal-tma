import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Django ni to'liq ishga tushir
django.setup()

# Jadvallar yo'q bo'lsa yaratish + seed data
from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=1)
except Exception as e:
    print(f"[wsgi] migrate error: {e}")

try:
    call_command('seed_data', verbosity=0)
except Exception as e:
    print(f"[wsgi] seed_data error: {e}")

application = get_wsgi_application()
