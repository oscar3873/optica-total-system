from django.urls import path

from .views import NoteCreateView,NoteListView, LabelCreateView
app_name = 'note_app'


urlpatterns = [
    path(
        'new/',
        NoteCreateView.as_view(),
        name='new_note'
    ),

    path(
        'list/note',
        NoteListView.as_view(),
        name='note_list'
    ),

    path(
        'new/label',
        LabelCreateView.as_view(),
        name='new_label'
    ),
]