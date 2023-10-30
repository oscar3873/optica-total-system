from datetime import timedelta
from django.views.generic import TemplateView

from project.settings.base import DATE_NOW
from applications.sales.models import *
from applications.sales.forms import OrderDetailForm

from applications.core.models import Objetives

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/general_reports.html'

    def get_context_data(self, **kwargs):
        contex=super().get_context_data(**kwargs)
        contex['employee_objectives'] = Objetives.objects.filter(to='EMPLEADOS')
        contex['total_semanal']=20
        return contex
    
class DailyReportsView(TemplateView):
    template_name = 'dashboard/daily_summary.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)

        week_date = DATE_NOW.date() - timedelta(days=7)

        sale = Sale.objects.filter(created_at__gte=week_date, created_at__lte=DATE_NOW.date(), branch=branch_actualy)

        week_sales = {
            'lun': [0, 0],
            'mar': [0, 0],
            'mie': [0, 0],
            'jue': [0, 0],
            'vie': [0, 0],
            'sab': [0, 0],
            'dom': [0, 0]
        }
        
        for day in week_sales:
            dia_semana = sale.created_at.strftime('%a').lower()
            week_sales[dia_semana][0] += sale.total
            week_sales[dia_semana][1] += OrderDetail.objects.filter(sale=sale).count()

        context['week_sales'] = week_sales
        return context
    
