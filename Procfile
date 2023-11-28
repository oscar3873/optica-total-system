web: daphne project.project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=project.project.settings.prod -v2