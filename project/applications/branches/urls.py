from django.urls import path
from .views import BranchCreateView,BranchListView,BranchUpdateView

app_name = 'branches_app'

urlpatterns = [
    path(
        'new/', 
        BranchCreateView.as_view(),
        name='new_branch'
    ),

    #UPDATE

    path(
        'update/branch/<pk>/',
        BranchUpdateView.as_view(),
        name='update_branch',
    ),

    #LISTING
    
    path(
        'list/branch',
        BranchListView.as_view(),
        name='branch_list'
    ),
]
