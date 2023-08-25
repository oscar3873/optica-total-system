from django.urls import path
from .views import CustomerCreateView, HealthInsuranceCreateView, CalibrationOrderCreateView
app_name = 'clients_app'

urlpatterns = [
    path(
        'new/customer/', 
        CustomerCreateView.as_view(),
        name='new_customer'
    ),
    path(
        'new/health_insurance/',  
        HealthInsuranceCreateView.as_view(),
        name='new_hi'
    ),
    path(
        'new/lab/',  
        CalibrationOrderCreateView.as_view(), 
        name='new_laboratory'
    ),
]
