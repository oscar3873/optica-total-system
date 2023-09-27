from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/general_reports.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contex=super().get_context_data(**kwargs)
        contex['total_semanal']=20
        return contex
    
class DailyReportsView(TemplateView):
    template_name = 'dashboard/daily_summary.html'
