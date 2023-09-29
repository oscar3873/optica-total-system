from django.urls import path

from .views import DailyReportsView, DashboardView

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
    )
]



