from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from applications.core.mixins import CustomUserPassesTestMixin, LoginRequiredMixin
from .models import *
from .forms import *

# Create your views here.

#################################### CREATE ####################################
class PromotionCreateView(CustomUserPassesTestMixin, FormView):
    form_class = PromotionProductForm  # Utiliza el nuevo formulario
    template_name = 'promotions/promotions_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        # Procesar el formulario y asociar productos a la promoción
        promotion = form.save()  # Guarda la promoción en la base de datos
        selected_products = form.cleaned_data.get('products')
        for product in selected_products:
            PromotionProduct.objects.create(promotion=promotion, product=product)
        #messages.success(self.request, 'Promoción creada exitosamente.')
        return super().form_valid(form)


#################################### DETAILS ####################################
class PromotionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'promotions/promotion_detail.html'
    model = Promotion
    
    def get(self, request, *args, **kwargs):
        user = request.user
        branch = user.branch
        object = self.get_object()

        if not user.is_staff and not object.branch == branch: 
            # El usuario no tiene permiso para ver este producto
            messages.error(request, 'Lo sentimos, no puedes ver esta promocion.')
            return redirect('promotions_app:promotion_list')  # Reemplaza 'nombre_de_tu_vista_product_list' por el nombre correcto de la vista de lista de productos
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aquí puedes agregar los datos que desees al contexto
        # Por ejemplo, obtener los productos asociados a la promoción actual
        promotion = self.get_object()
        associated_products = promotion.promotion_products.all()
        context['associated_products'] = associated_products
        return context

#################################### UPDATE ####################################
class PromotionUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Promotion  # Especifica el modelo a actualizar
    form_class = PromotionProductForm  # Utiliza el mismo formulario que la vista de creación
    template_name = 'promotions/promotion_update.html'  # La plantilla para la página de actualización
    success_url = reverse_lazy('core_app:home')  # URL de redirección exitosa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar datos adicionales al contexto si es necesario
        return context

    def form_valid(self, form):
        # Procesa el formulario de actualización
        promotion = form.save()  # Guarda la promoción actualizada
        selected_products = form.cleaned_data.get('products')
        PromotionProduct.objects.filter(promotion=promotion).delete()  # Elimina las relaciones anteriores
        for product in selected_products:
            PromotionProduct.objects.create(promotion=promotion, product=product)  # Crea las nuevas relaciones
        return super().form_valid(form)
    
#################################### LIST ####################################
class PromotionListView(LoginRequiredMixin, ListView):
    model = Promotion
    template_name = 'promotions/promotion_list.html'
    context_object_name = 'promotions'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            branch_actualy = self.request.session.get('branch_actualy')
            branch_actualy = Branch.objects.get(id=branch_actualy)
            branch = branch_actualy
        else:
            branch = user.branch

        return Promotion.objects.filter(branch=branch)  # Filtra las promociones según la sucursal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_fields = ['name', 'type_prom__name', 'description', 'start_date', 'end_date']
        context['custom_promotions'] = Promotion.objects.filter(branch=self.get_queryset().first().branch).values(*custom_fields)
        return context


# def ajax_promotional_products(request):
#     branch = request.user.branch

#     branch_actualy = request.session.get('branch_actualy')
#     if request.user.is_staff and branch_actualy:
#         branch = Branch.objects.get(id=branch_actualy)

#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

#         list_promotion = { # Lista de promociones con sus respectivos productos asociados
#             'A' : ['1', '2', '3'], # 2x1
#             'B' : ['4', '5'],      # 50% off
#             'C' : [''],            # descuento %
#         }
#         # Crear una lista de diccionarios con los datos de los empleados
#         return JsonResponse({'promotions': list_promotion})
# comentado ajax viejo

def ajax_promotional_products(request):
    branch = request.user.branch

    branch_actualy = request.session.get('branch_actualy')
    if request.user.is_staff and branch_actualy:
        branch = Branch.objects.get(id=branch_actualy)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        
        promotions = Promotion.objects.all()  # Obtén todas las promociones
        list_promotion = {}

        for promotion in promotions:
            # Obtén los productos asociados a cada promoción
            associated_products = promotion.promotion_products.values_list('product__name', flat=True)
            list_promotion[promotion.name] = list(associated_products)

        return JsonResponse({'promotions': list_promotion})