web: daphne project.project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=project.settings.prod -v2