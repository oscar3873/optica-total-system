web: daphne project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
worker: python project/manage.py runworker --settings=project.settings.prod -v2
