from django.urls import path, include
#
from . import views

app_name = 'users_app'

urlpatterns = [
    path(
        'signup/',
        views.UserCreateView.as_view(),
        name = 'signup'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name = 'login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name = 'logout'
    ),
        path(
        'update_password/',
        views.UpdatePasswordView.as_view(),
        name = 'update_password'
    ),
]
