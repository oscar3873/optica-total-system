import json
from typing import Any
from django import http
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
import json

#Importaciones de la app
from applications.branches.models import Branch
from .models import *
from .forms import *


# Create your views here.
class PointOfSaleView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/point_of_sale_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch = Branch.objects.get(id=branch_actualy)
        except Branch.DoesNotExist:
            branch = self.request.user.branch

        context['branch_selected'] = branch.name
        return context
    

class PayView(View):
    template_name = 'sales/pay_page.html'

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            seleccionados = data.get('seleccionados', [])
            return seleccionados
        except json.JSONDecodeError:
            return []
        

class SalesPayView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_data = data.get('seleccionados', [])

            # Crear instancias de OrderDetail a partir de los datos recibidos
            order_details = []
            for item in selected_data:
                product_id = item['productId']
                quantity = item['quantity']
                
                # Buscar el producto en base a su ID
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return http.JsonResponse({'error': f'El producto con ID {product_id} no existe'}, status=400)
                
                # Crear la instancia de OrderDetail y agregarla a la lista
                order_detail = OrderDetail(product=product, quantity=quantity)
                order_details.append(order_detail)
            
            # Guardar las instancias de OrderDetail en la base de datos
            OrderDetail.objects.bulk_create(order_details)
            
            # Puedes devolver una respuesta JSON como confirmación
            response_data = {'mensaje': 'Valores procesados correctamente'}
            return http.JsonResponse(response_data)
        except json.JSONDecodeError:
            return http.JsonResponse({'error': 'Error al procesar los datos'}, status=400)
