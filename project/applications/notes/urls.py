from django.urls import path

from .views import NoteCreateView, index, room

app_name = 'note_app'


urlpatterns = [
    path(
        'new/',
        NoteCreateView.as_view(),
        name='new_note'
    ),
    path(
        '',
        index,
        name='index'
    ),
    path(
        "<str:room_name>/",
        room,
        name="room"),
]