#
from django.urls import path
# Views basadas en clases
from .views import HomePageView

app_name = 'core_app'

urlpatterns = [
    path('', 
        HomePageView.as_view(), 
        name='home'
    ),
] 