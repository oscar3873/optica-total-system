from django.urls import path

from .views import NoteCreateView
app_name = 'note_app'


urlpatterns = [
    path(
        'new/',
        NoteCreateView.as_view(),
        name='new_note'
    ),
]