from django.http import JsonResponse
from django.views.generic import TemplateView

from project.settings import DATE_NOW
from branches.utils import set_branch_session

from .utils import *

fecha_hoy = DATE_NOW.date()


# Create your views here.
class DailyReportsView(TemplateView):
    template_name = 'dashboard/daily_summary.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        
        branch_actualy = set_branch_session(self.request)
        
        context['monto_por_rango_completado'], context['monto_por_rango_pendiente'] = dayli_sales(branch_actualy) # 8am a 9pm : $ventas
        context['customers'] = dayli_customers(branch_actualy) # clientes registrados del dia
        context['sales'] = dayli_sales_count(branch_actualy) # cantidad de ventas del dia
        context['suma_total_ventas'] = dayli_sales_total(branch_actualy) # total en $ventas del dia
        context['suma_total_ventas_ayer'] = yesterday_sales_total(branch_actualy) # tota en ventas del dia anterior
        context['columns_sale'], context['sale_list'] = list_sale_to_dayli(branch_actualy) # lista de ventas para tabla ¡¡<<VER: CARLOS PUTOOO>>!!
        context['columns_mov'], context['mov_list'] = movs_to_dayli(branch_actualy) # lista de ventas para tabla ¡¡<<VER: CARLOS PUTOOO>>!!
        
        return context
    
class DashboardView(TemplateView):
    template_name = 'dashboard/general_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      
        branch_actualy = set_branch_session(self.request)

        context['ventas_semanales'] = week_status(branch_actualy) # devuleve un diccionario con las ventas de la semana
        context['ventas_por_semana'], context['total_ventas_anteriores'], context['ventas_anteriores'], context['total_ventas_semana_anterior'] = week_sales(branch_actualy) # devuleve un diccionario con las ventas de la semana
        context['productos_mas_vendidos'] = top_prodcuts(branch_actualy) # devuleve un diccionario con el TOP de prodcutos mas vendidos
        context['marcas_mas_vendidos'] = top_brands(branch_actualy) # devuleve un diccionario con el TOP de marcas mas vendidas
        context['objetivos_emp'], context['objetivos_suc'] = objetives(branch_actualy) # VER MODELO PARA ACCEDER A LOS CAMPOS NECESARIOS!!!

        return context
    


def sale_date_month(request, month):
    from calendar import monthrange
    # Obtener el primer y último día del mes

    if request.method == 'GET':
        if 1 <= int(month) <= 12:
            _, ultimo_dia = monthrange(fecha_actual.year, month)

            ventas_por_dia = []

            branch_actualy = set_branch_session(request)

            for dia in range(1, ultimo_dia + 1):
                fecha_actual = datetime(fecha_actual.year, month, dia)
                ventas_dia = Sale.objects.filter(created_at__date=fecha_actual, branch=branch_actualy).count()
                ventas_por_dia.append((dia, ventas_dia))

            return JsonResponse({'status': 'success', 'data': ventas_por_dia})
        else:
            return JsonResponse({'status': 'error', 'message': 'El mes proporcionado no existe.'})