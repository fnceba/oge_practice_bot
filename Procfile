release: python manage.py migrate --noinput
bot: python run_pooling.py
web: gunicorn --bind :$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker oge_practice.asgi:application
worker: celery -A oge_practice worker -P prefork --loglevel=INFO 
beat: celery -A oge_practice beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
