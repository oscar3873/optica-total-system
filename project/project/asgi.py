"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
import sys

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from pathlib import Path


# Agregar el directorio del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(BASE_DIR)


# application = get_asgi_application() # Original

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django.setup()
django_asgi_app = get_asgi_application()

from applications.core.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)