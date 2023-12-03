from collections import defaultdict
from datetime import timedelta
from django.db.models import Sum, F
from datetime import datetime, time

from django.utils import timezone
from products.models import Brand, Product
from clients.models import Customer
from sales.models import Sale
from cashregister.models import Movement
from employes.models import Employee_Objetives
from branches.models import Branch_Objetives

fecha_hoy = timezone.now().date()


##############################  REPORTES DE SEMANAS  #############################

def week_status(branch_actualy):
    # week_date = fecha_hoy - timedelta(weeks=1)

    week_date = fecha_hoy - timedelta(days=fecha_hoy.weekday())
    
    sale = Sale.objects.filter(created_at__date__gte=week_date, created_at__date__lte=fecha_hoy,
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
    
    # Supongamos que 'created_at' es un objeto datetime en UTC
    
    for day in week_sales:
        for s in sale:
            # Convierte la fecha y hora de UTC a la zona horaria de Argentina
            created_at= s.created_at
            dia_semana = created_at.strftime('%a').lower()
            if day in dia_semana.lower():
                week_sales[day][0] += round(float(s.total))
                week_sales[day][1] += 1

    return week_sales

def week_sales(branch_actualy):
    # Obtener la fecha de hoy
    # Calcular la fecha de inicio de la semana actual (lunes)
    fecha_inicio_semana_actual = fecha_hoy - timedelta(days=fecha_hoy.weekday())
    # Calcular la fecha de inicio de las 3 semanas anteriores (y la actual)
    fecha_inicio_cuatro_semanas = fecha_inicio_semana_actual - timedelta(weeks=3)

    # Lista para almacenar las ventas por semana
    ventas_por_semana = []

    # Calcular las ventas de las 4 semanas (incluyendo la semana actual)
    for i in range(4):
        fecha_inicio_semana = fecha_inicio_cuatro_semanas + timedelta(weeks=i)
        fecha_fin_semana = fecha_inicio_semana + timedelta(days=5)  # Sumar 5 días para llegar al sábado (excluir el domingo)
        ventas_semana = Sale.objects.filter(branch=branch_actualy,
            created_at__range=(fecha_inicio_semana, fecha_fin_semana)
        ).count()
        ventas_por_semana.append((i + 1, ventas_semana))

    # Calcular el total de ventas de las 4 semanas (incluyendo la actual)
    total_ventas = Sale.objects.filter(branch=branch_actualy,
                            created_at__range=(fecha_inicio_cuatro_semanas, fecha_fin_semana)
                        ).count()

    ventas_totales = Sale.objects.filter(branch=branch_actualy,
                            created_at__range=(fecha_inicio_cuatro_semanas, fecha_fin_semana)
                        ).aggregate(total_ventas=Sum('total'))
    
    total_ventas_semana_anterior = Sale.objects.filter(branch=branch_actualy,
                            created_at__range=(fecha_inicio_semana_actual - timedelta(weeks=1), fecha_inicio_semana_actual - timedelta(days=1))
                        ).aggregate(total_ventas=Sum('total'))['total_ventas']


    return ventas_por_semana, int(ventas_totales['total_ventas'] or 0), total_ventas, total_ventas_semana_anterior or 0


def top_prodcuts(branch_actualy):
    # Obtén un diccionario con el nombre del producto y la cantidad total vendida
    productos_mas_vendidos = Product.objects.annotate(
        total_quantity_vendida=Sum('order_detaill__quantity')
    ).exclude(
        name__icontains='propio').exclude(category__name__icontains='Cristal'
    ).filter(total_quantity_vendida__gt=0, branch=branch_actualy).values('name', 'brand__name', 'total_quantity_vendida')[:5]

    top_productos_mas_vendidos = {}

    # Llena el diccionario con el nombre del producto y la cantidad total vendida
    for producto in productos_mas_vendidos:
        top_productos_mas_vendidos[producto['name']] = (producto['brand__name'], producto['total_quantity_vendida'])

    # Puedes ordenar el diccionario por la cantidad vendida si es necesario
    top_productos_mas_vendidos = dict(sorted(top_productos_mas_vendidos.items(), key=lambda item: item[1], reverse=True))
    return top_productos_mas_vendidos


def top_brands(branch_actualy):
    # Obtén un diccionario con el nombre de la marca y la cantidad total vendida
    marcas_mas_vendidas = Brand.objects.filter(product_brand__branch=branch_actualy
            ).annotate(total_cantidad_vendida=Sum('product_brand__order_detaill__quantity')
            ).exclude(
                product_brand__name__icontains='propio'
            ).filter(total_cantidad_vendida__gt=0).values('name', 'total_cantidad_vendida')[:5]

    # Crea un diccionario para almacenar los resultados
    top_marcas_mas_vendidas = defaultdict(int)

    # Llena el diccionario con el nombre de la marca y la cantidad total vendida
    for marca in marcas_mas_vendidas:
        top_marcas_mas_vendidas[marca['name']] += marca['total_cantidad_vendida']

    # Ordena el diccionario por la cantidad total vendida en orden descendente
    top_marcas_mas_vendidas = dict(sorted(top_marcas_mas_vendidas.items(), key=lambda item: item[1], reverse=True))

    # Imprime el diccionario
    return top_marcas_mas_vendidas # TOP MARCAS +VENDIDAS


def objetives(branch_actualy):
    obj_employee = Employee_Objetives.objects.filter(employee__user__branch=branch_actualy, objetive__exp_date__gte=fecha_hoy, deleted_at=None).order_by('employee', 'created_at').distinct('employee')
    obj_branch = Branch_Objetives.objects.filter(branch=branch_actualy, objetive__exp_date__gte=fecha_hoy, deleted_at=None).order_by('branch', 'created_at').distinct('branch')

    return obj_employee, obj_branch

######################## REPORTES DIARIOS #########################

def dayli_sales(branch_actualy):
    # Crea una lista de horas en el rango de 8 a.m. a 9 p.m.
    horas = [datetime.combine(timezone.now(), time(i, 0)) for i in range(8, 22)]
    # Inicializa diccionarios para almacenar los montos recaudados en cada intervalo de una hora
    monto_por_rango_completado = {str(hora.hour): 0 for hora in horas}
    monto_por_rango_pendiente = {str(hora.hour): 0 for hora in horas}

    # Realiza la consulta para obtener los montos recaudados en cada hora con estado "COMPLETADO"
    ventas_completadas = Sale.objects.filter(created_at__date=fecha_hoy, state='COMPLETADO', branch=branch_actualy,
                                            deleted_at=None).values('created_at__time').annotate(monto_recaudado=Sum('sale_payment__amount'))
    
    # Realiza la consulta para obtener los montos recaudados en cada hora con estado "PENDIENTE"
    ventas_pendientes = Sale.objects.filter(created_at__date=fecha_hoy, state='PENDIENTE', branch=branch_actualy,
                                            deleted_at=None).values('created_at__time').annotate(monto_recaudado=Sum(F('total') - F('missing_balance')))

    # Llena los diccionarios con los montos recaudados en cada intervalo de una hora
    for venta in ventas_completadas:
        hora_venta = venta['created_at__time']
        monto_recaudado = venta['monto_recaudado']
        
        for i in range(len(horas) - 1):
            if horas[i].time() <= hora_venta < horas[i + 1].time():
                monto_por_rango_completado[str(horas[i].hour)] += float(monto_recaudado)
                break

    for venta in ventas_pendientes:
        hora_venta = venta['created_at__time']
        monto_recaudado = venta['monto_recaudado']
        
        for i in range(len(horas) - 1):
            if horas[i].time() <= hora_venta < horas[i + 1].time():
                monto_por_rango_pendiente[str(horas[i].hour)] += float(monto_recaudado)
                break
    

    return monto_por_rango_completado, monto_por_rango_pendiente


def dayli_customers(branch_actualy):
    customers = Customer.objects.filter(created_at__date=fecha_hoy, branch=branch_actualy).count()
    return customers


def dayli_sales_count(branch_actualy):
    sales = Sale.objects.filter(created_at__date=fecha_hoy, branch=branch_actualy).count()
    return sales


def dayli_sales_total(branch_actualy):
    suma_total = Sale.objects.filter(created_at__date=datetime.now().date(), branch=branch_actualy).aggregate(suma_total_ventas=Sum(F('sale_payment__amount')))
    suma_total_ventas = suma_total['suma_total_ventas'] if suma_total['suma_total_ventas'] is not None else 0
    return suma_total_ventas


def yesterday_sales_total(branch_actualy):
    suma_total = Sale.objects.filter(created_at__date=datetime.now().date() - timedelta(days=1), branch=branch_actualy).aggregate(suma_total_ventas=Sum(F('sale_payment__amount')))
    suma_total_ventas = suma_total['suma_total_ventas'] if suma_total['suma_total_ventas'] is not None else 0
    return suma_total_ventas


def list_sale_to_dayli(branch_actualy):
    """
    IDEA: MOSTRAR COMO INDICA EN LA VARIABLE columns,
          link a el Cliente y a Venta
    """
    columns = ['Por', 'Fecha', 'Hora', 'Cliente', 'Estado', 'Total']

    sale = Sale.objects.filter(branch=branch_actualy).order_by('-created_at')[:4] # campos qeu se deben mostrar en la tabla: sale.id, sale.created_at, sale.state, sale.total, sale.customer
    return columns, sale


def movs_to_dayli(branch_actualy):
    columns = ['Por', 'Fecha', 'Hora', 'Descripción', 'Tipo', 'Monto'] # MODIFICAR 

    moviments = Movement.objects.filter(cash_register__branch=branch_actualy).order_by('-created_at')[:4]
    
    return columns, moviments