from django.urls import re_path

from .consumers import NoteConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/global/$", NoteConsumer.as_asgi()),
]