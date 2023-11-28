web: daphne project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2 --root-path=project
chatworker: python manage.py runworker --settings=project.settings.prod -v2