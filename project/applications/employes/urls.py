from django.urls import path
from .views import EmployeeCreateView, EmployeeProfileView, EmployeeUpdateView

app_name = 'employees_app'

urlpatterns = [
    path(
        'new/', 
        EmployeeCreateView.as_view(),
        name='new'
    ),
    path(
        'profile/<pk>/', 
        EmployeeProfileView.as_view(),
        name='profile'
    ),
    path(
        'update/<pk>/',
        EmployeeUpdateView.as_view(),
        name='update'
    ),
]
