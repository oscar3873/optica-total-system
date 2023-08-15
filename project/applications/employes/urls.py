from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

#
from . import views

app_name = 'employees_app'

urlpatterns = [
    path(
        'new/', 
        views.EmployeeCreateView.as_view(),
        name='new' # consumir en template con user.pk
    ),
    path(
        'profile/<pk>/', 
        views.EmployeeProfileView.as_view(),
        name='profile' # consumir en template con user.pk
    ),
]