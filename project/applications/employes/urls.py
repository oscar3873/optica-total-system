from django.urls import path
from .views import (
    EmployeeProfileView,
    EmployeeListView,
    EmployeeCreateView,
    EmployeeDeleteView,
    AccountView,
    EmployeeUpdateView
    )

app_name = 'employees_app'

urlpatterns = [
    path(
        'new/', 
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
        'list/',
        EmployeeListView.as_view(),
        name='list_employee'
    ),
    path(
        'delete/<pk>/',
        EmployeeDeleteView.as_view(),
        name='employee_delete'
    ),
    path(
        'account/<int:pk>/', 
        AccountView.as_view(), 
        name='account'
    ),
    
]
