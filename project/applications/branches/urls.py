from django.urls import path
from .views import BranchCreateView

app_name = 'branches_app'

urlpatterns = [
    path(
        'new/', 
        BranchCreateView.as_view(),
        name='new_branch'
    ),
]
