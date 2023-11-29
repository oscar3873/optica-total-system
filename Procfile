web: --root-path=/project/project daphne project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
chatworker: PYTHONPATH=/project/project python project/manage.py runworker --settings=project.settings -v2
