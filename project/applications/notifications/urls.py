from django.urls import path

from .views import NotificationsCreateView, NotificationsListView, DynamicDetail, LoadNotificationsView

app_name = 'notifications_app'

urlpatterns = [
    path(
        'new/',
        NotificationsCreateView.as_view(),
        name='new'
    ),
    path(
        'list/',
        NotificationsListView.as_view(),
        name='list'
    ),
    path(
        'dynamic_detail/<str:model_name>/<int:pk>/',
        DynamicDetail.as_view(),
        name='dynamic_detail'
        ),
    path(
        'load/',
        LoadNotificationsView.as_view(),
        name='load_notifications'
    )
]