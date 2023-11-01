from django.urls import path

from .views import *

app_name = 'dashboard_app'

urlpatterns = [
    path(
        'reports/general',
        DashboardView.as_view(),
        name='home'
    ),
    path(
        'reports/daily',
        DailyReportsView.as_view(),
        name='daily_summary'
    ),

    ####### AJAX MOTHN DATA ########
    path(
        'sale_date_month/<month>/',
        sale_date_month,
        name='sale_date_month'
    )
]



