from django.urls import path
from .views import EmployeeProfileView

app_name = 'employees_app'

urlpatterns = [
    # path(
    #     'new/', 
    #     EmployeeCreateView.as_view(),
    #     name='new_employee'
    # ),
    # path(
    #     'update/<pk>/',
    #     EmployeeUpdateView.as_view(),
    #     name='update_employee'
    # ),
    path(
        'profile/<pk>/', 
        EmployeeProfileView.as_view(),
        name='profile_employee'
    ),
]
