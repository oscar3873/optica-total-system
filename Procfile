web: daphne project.asgi:application -u project/asgi.py -p $REDIS_PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker