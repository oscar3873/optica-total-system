web: daphne project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=project.settings -v2