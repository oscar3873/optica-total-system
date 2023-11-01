from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Sum, F


from project.settings.base import DATE_NOW
from applications.sales.models import *
from applications.core.models import Objetives

from .utils import *

fecha_hoy = DATE_NOW.date()


# Create your views here.
class DailyReportsView(TemplateView):
    template_name = 'dashboard/daily_summary.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)
        
        context['employee_objectives'] = Objetives.objects.filter(to='EMPLEADOS')

        context['monto_por_rango_completado'], context['monto_por_rango_pendiente'] = dayli_sales(context, branch_actualy) # 8am a 9pm : $ventas
        context['customers'] = dayli_customers(context, branch_actualy) # clientes registrados del dia
        context['sales'] = dayli_sales_count(context, branch_actualy) # cantidad de ventas del dia
        context['suma_total_ventas'] = dayli_sales_total(context, branch_actualy) # total en $ventas del dia
        context['columns_sale'], context['sale_list'] = list_sale_to_dayli(context, branch_actualy) # lista de ventas para tabla ¡¡<<VER: CARLOS PUTOOO>>!!
        context['columns_mov'], context['mov_list'] = movs_to_dayli(context, branch_actualy) # lista de ventas para tabla ¡¡<<VER: CARLOS PUTOOO>>!!
        
        return context
    
class DashboardView(TemplateView):
    template_name = 'dashboard/general_reports.html'
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)

        context['week_sales'] = week_status(context, branch_actualy) # devuleve un diccionario con las ventas de la semana
        context['ventas_por_semana'], context['total_ventas_anteriores'] = week_sales(context, branch_actualy) # devuleve un diccionario con las ventas de la semana
        context['productos_mas_vendidos'] = top_prodcuts(context, branch_actualy) # devuleve un diccionario con el TOP de prodcutos mas vendidos
        context['marcas_mas_vendidos'] = top_brands(context, branch_actualy) # devuleve un diccionario con el TOP de marcas mas vendidas

        return context
    


def sale_date_month(request, numero_mes):
    from calendar import monthrange
    # Obtener el primer y último día del mes
    _, ultimo_dia = monthrange(DATE_NOW.year, numero_mes)

    ventas_por_dia = []

    for dia in range(1, ultimo_dia + 1):
        fecha_actual = datetime(DATE_NOW.now().year, numero_mes, dia)
        ventas_dia = Sale.objects.filter(created_at__date=fecha_actual).count()
        ventas_por_dia.append((dia, ventas_dia))

    return JsonResponse({'data': ventas_por_dia})