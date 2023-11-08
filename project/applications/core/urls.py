#
from django.urls import path
# Views basadas en clases
from .views import *

app_name = 'core_app'

urlpatterns = [
    path('', 
        HomePageView.as_view(), 
        name='home'
    ),

    path(
        'objetives/new/', 
        ObjetiveCreateView.as_view(), 
        name='objetive_new'
    ),

    path(
        'objetives/update/<pk>/', 
        ObjetiveUpdateView.as_view(),
        name='objetive_update'
    ),

    path(
        'objetives/list/',
        ObjetivesListView.as_view(),
        name='objetive_list'
    ),

] 