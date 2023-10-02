from django.urls import path
from .views import *

app_name = 'employees_app'

urlpatterns = [
    path(
        'signup/', 
        EmployeeCreateView.as_view(),
        name='new_employee'
    ),
    path(
        'update/<pk>/',
        EmployeeUpdateView.as_view(),
        name='update_employee'
    ),
    path(
        'profile/<pk>/', 
        EmployeeProfileView.as_view(),
        name='profile_employee'
    ),
    path(
        '',
        EmployeeListView.as_view(),
        name='list_employee'
    ),
    path(
        'delete/<pk>/',
        EmployeeDeleteView.as_view(),
        name='employee_delete'
    ),

]
