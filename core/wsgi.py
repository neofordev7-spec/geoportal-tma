import os
import shutil
from pathlib import Path
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from django.conf import settings
from django.core.management import call_command

# Migrate
try:
    call_command('migrate', '--noinput', verbosity=1)
    print("[wsgi] Migrate done")
except Exception as e:
    print(f"[wsgi] Migrate error: {e}")

# Seed
try:
    call_command('seed_data', verbosity=1)
    print("[wsgi] Seed done")
except Exception as e:
    print(f"[wsgi] Seed error: {e}")

# Media fayllarni nusxalash (video/rasm — static emas, media orqali serve)
src = settings.BASE_DIR / 'video_rasmlar'
dst = settings.MEDIA_ROOT / 'lenta'
dst.mkdir(parents=True, exist_ok=True)
FILES = {
    'qarshi_yakkaboq.mp4': src / 'qarshi_yakkaboq.mp4',
    'asfalt.mp4': src / 'asfalt.mp4',
    'kocha.jpg': src / 'problem_image' / 'kocha.jpg',
    'kocha3.jpg': src / 'problem_image' / 'kocha 3.jpg',
    'kochaq.jpg': src / 'problem_image' / 'kochaq.jpg',
}
for name, s in FILES.items():
    d = dst / name
    if s.exists() and not d.exists():
        shutil.copy2(s, d)
        print(f"[wsgi] Copied {name}")

application = get_wsgi_application()
