from django.urls import path

from .views import NotificationsCreateView

app_name = 'notifications_app'

urlpatterns = [
    path(
        'new/',
        NotificationsCreateView.as_view(),
        name='new_notifications'
    ),
    path(
        'list/',
        NotificationsCreateView.as_view(),
        name='list_notifications'
    )
]