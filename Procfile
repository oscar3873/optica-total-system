web: PYTHONPATH=/optica-total/project daphne --root-path=/project/project project.asgi:application --port $REDIS_PORT --bind 0.0.0.0 -v2
chatworker: PYTHONPATH=/optica-total/project python project/manage.py runworker --settings=project.settings -v2
