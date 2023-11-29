web: daphne --root-path=/project/project project.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python project/manage.py runworker --settings=project.settings -v2