from django.urls import path
from .views import CustomerCreateView

app_name = 'clients_app'

urlpatterns = [
    path(
        'new/', 
        CustomerCreateView.as_view(),
        name='new_customer'
    ),
]
