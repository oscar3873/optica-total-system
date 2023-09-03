from django.urls import re_path

from .consumers import NoteConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notes/global/$", NoteConsumer.as_asgi()),
    re_path(r"ws/notifications/global/$", NotificationConsumer.as_asgi()),
]