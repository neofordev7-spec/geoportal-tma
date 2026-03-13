web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_data && python -m gunicorn core.wsgi --bind 0.0.0.0:$PORT --workers 2
worker: python bot/bot.py
