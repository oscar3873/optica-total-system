from datetime import timedelta
from django.http import JsonResponse
from django.views.generic import TemplateView

from applications.products.models import Brand

from project.settings.base import DATE_NOW
from applications.sales.models import *

from applications.core.models import Objetives

from django.db.models import Sum, F, Value, Count
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractHour
from collections import defaultdict
from datetime import datetime, time

# Create your views here.
class DailyReportsView(TemplateView):
    template_name = 'dashboard/daily_summary.html'

    def get_context_data(self, **kwargs):

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)

        contex=super().get_context_data(**kwargs)
        contex['employee_objectives'] = Objetives.objects.filter(to='EMPLEADOS')

        # Crea una lista de horas en el rango de 8 a.m. a 9 p.m.
        horas = [datetime.combine(DATE_NOW.now(), time(i, 0)) for i in range(8, 22)]

        # Inicializa diccionarios para almacenar los montos recaudados en cada intervalo de una hora
        monto_por_rango_completado = {str(hora.hour): 0 for hora in horas}
        monto_por_rango_pendiente = {str(hora.hour): 0 for hora in horas}

        # Realiza la consulta para obtener los montos recaudados en cada hora con estado "COMPLETADO"
        ventas_completadas = Sale.objects.filter(created_at__date=DATE_NOW.now(), state='COMPLETADO', branch=branch_actualy).values('created_at').annotate(monto_recaudado=Sum('total'))

        # Realiza la consulta para obtener los montos recaudados en cada hora con estado "PENDIENTE"
        ventas_pendientes = Sale.objects.filter(created_at__date=DATE_NOW.now(), state='PENDIENTE', branch=branch_actualy).values('created_at').annotate(monto_recaudado=Sum(F('total') - F('missing_balance')))

        # Llena los diccionarios con los montos recaudados en cada intervalo de una hora
        for venta in ventas_completadas:
            hora_venta = venta['created_at']
            monto_recaudado = venta['monto_recaudado']
            
            for i in range(len(horas) - 1):
                if horas[i] <= hora_venta < horas[i + 1]:
                    monto_por_rango_completado[str(horas[i].hour)] += monto_recaudado
                    break

        for venta in ventas_pendientes:
            hora_venta = venta['created_at']
            monto_recaudado = venta['monto_recaudado']
            
            for i in range(len(horas) - 1):
                if horas[i] <= hora_venta < horas[i + 1]:
                    monto_por_rango_pendiente[str(horas[i].hour)] += monto_recaudado
                    break
        
        print('\n\n\n\'',monto_por_rango_completado)
        print('\n\n\n\'',monto_por_rango_pendiente)
        contex['monto_por_rango_completado'] = monto_por_rango_completado
        contex['monto_por_rango_pendiente'] = monto_por_rango_pendiente


        customers = Customer.objects.filter(created_at__date=DATE_NOW.date(), branch=branch_actualy).count()
        print('\n\n\n\'',customers)
        contex['customers'] = customers


        sales = Sale.objects.filter(created_at__date=DATE_NOW.date(), branch=branch_actualy).count()
        print('\n\n\n\'',sales)
        contex['sales'] = sales


        suma_total = Sale.objects.filter(created_at__date=datetime.now().date(), branch=branch_actualy).aggregate(suma_total_ventas=Sum(F('total') - F('missing_balance')))
        contex['suma_total_ventas'] = suma_total['suma_total_ventas'] if suma_total['suma_total_ventas'] is not None else 0
        print('\n\n\n\'',contex['suma_total_ventas'])


        return contex
    
class DashboardView(TemplateView):
    template_name = 'dashboard/general_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)

        week_date = DATE_NOW.date() - timedelta(days=7)

        sale = Sale.objects.filter(created_at__date__gte=week_date, created_at__date__lte=DATE_NOW.date(),
                                   branch=branch_actualy, deleted_at=None)

        week_sales = {
            'mon': [0, 0],
            'tue': [0, 0],
            'wen': [0, 0],
            'thu': [0, 0],
            'fri': [0, 0],
            'sat': [0, 0],
            'sun': [0, 0]
        }
        
        for day in week_sales:
            for s in sale:
                dia_semana = s.created_at.strftime('%a').lower()
                print(dia_semana)
                if day in dia_semana.lower():
                    print(s)
                    week_sales[day][0] += float(s.total)
                    week_sales[day][1] += OrderDetail.objects.filter(sale=s).count()

        context['week_sales'] = week_sales
        print(week_sales)



        fecha_hoy = datetime.now()
        fecha_inicio = fecha_hoy - timedelta(weeks=4)

        ventas_por_semana = []

        for i in range(4):
            fecha_inicio_semana = fecha_inicio + timedelta(weeks=i)
            fecha_fin_semana = fecha_inicio_semana + timedelta(weeks=1)
            ventas_semana = Sale.objects.filter(
                created_at__date__range=(fecha_inicio_semana.date(), fecha_fin_semana.date())
            ).count()
            ventas_por_semana.append((i + 1, ventas_semana))
        print(ventas_por_semana)


        productos_mas_vendidos = Product.objects.annotate(
                                num_sales=Count('order_detaill__sale')
                            ).filter(num_sales__gt=0).order_by('-num_sales')[:5]
        print(productos_mas_vendidos)
        context['productos_mas_vendidos'] = productos_mas_vendidos # TOP PRODUCTOS +VENDIDOS

        brands_with_sales = Brand.objects.annotate(
                            num_sales=Count('product_brand__order_detaill__sale')
                        ).filter(num_sales__gt=0).order_by('-num_sales')[:5]
        marcas_mas_vendidos = {brand.name: brand.num_sales for brand in brands_with_sales if brand.num_sales > 0}
        print(marcas_mas_vendidos)
        context['marcas_mas_vendidos'] = marcas_mas_vendidos # TOP MARCAS +VENDIDAS

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