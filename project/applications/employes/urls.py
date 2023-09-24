from django.urls import path
from .views import (
    EmployeeProfileView,
    EmployeeListView,
    EmployeeCreateView,
    EmployeeDeleteView,
    AccountView,
    EmployeeUpdateView,
    validate_password_current,
    UpdatePasswordView,
    UpdateUserInfoView,
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
    # Ruta para actualizar la información del usuario
    path('update_user_info/<int:pk>/', UpdateUserInfoView.as_view(), name='update_user_info'),

    # Ruta para actualizar la contraseña
    path('update_password/<int:pk>/', UpdatePasswordView.as_view(), name='update_password'),

    path(
        'validate_current_password/',
        validate_password_current,
        name='validate_current_password'
    ),
    
]
