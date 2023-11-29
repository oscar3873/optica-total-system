web: daphne -b 0.0.0.0 -p $REDIS_PORT --root-path=/project/project project.project.asgi:application
worker: python project/manage.py runworker --settings=project.settings.prod -v2
