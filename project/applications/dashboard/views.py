from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard_home.html'
