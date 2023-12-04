from django.urls import path

from .views import NoteCreateView,NoteListView, LabelCreateView, NoteUpdateView, NoteDeleteView
app_name = 'note_app'


urlpatterns = [
    path(
        'new/',
        NoteCreateView.as_view(),
        name='new_note'
    ),

    path(
        '',
        NoteListView.as_view(),
        name='note_list'
    ),

    path(
        'new/label',
        LabelCreateView.as_view(),
        name='new_label'
    ),

    path(
        'update/note/<pk>',
        NoteUpdateView.as_view(),
        name='update_note'
    ),

    path(
        'delete/note/<pk>',
        NoteDeleteView.as_view(),
        name='delete_note'
    )
]
