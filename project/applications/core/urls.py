#
from django.urls import path, include
# Views basadas en clases
from . import views


app_name = 'core_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]