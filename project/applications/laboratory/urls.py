from django.urls import path
from .views import LaboratoryCreateView

app_name = 'lab_app'

urlpatterns = [
    path(
        'new/', 
        LaboratoryCreateView.as_view(),
        name='new_lab'
    ),
]
