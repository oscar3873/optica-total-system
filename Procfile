web: gunicorn --pythonpath  project project.wsgi --log-file -
worker: gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$REDIS_PORT --pythonpath  project project.asgi:application