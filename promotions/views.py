from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages

from branches.utils import set_branch_session
from core.mixins import CustomUserPassesTestMixin, LoginRequiredMixin
from .models import *
from .forms import *
from cashregister.utils import obtener_nombres_de_campos
# Create your views here.

#################################### CREATE ####################################
class PromotionCreateView(CustomUserPassesTestMixin, FormView):
    form_class = PromotionProductForm
    template_name = 'promotions/promotions_page.html'
    success_url = reverse_lazy('promotions_app:promotion_list')

    def form_valid(self, form):
        # Crea la promoción sin guardarla en la base de datos aún
        promotion = form.save(commit=False)
        promotion.type_prom = form.cleaned_data.get('type_discount')
        
        user = self.request.user
        # Modificamos la forma de obtener la sucursal
        branch_actualy = set_branch_session(self.request)
        
        # Asignamos la sucursal a la promoción
        promotion.branch = branch_actualy

        # Guarda la promoción en la base de datos
        promotion.save()

        # Obtiene los productos seleccionados del formulario
        selected_products = form.cleaned_data.get('productsSelected')
        for product in selected_products:
            # Crea una relación entre la promoción y el producto
            PromotionProduct.objects.create(promotion=promotion, product=product)

        # Redirige a la página de inicio o a donde desees después de guardar
        return super().form_valid(form)



#################################### DETAILS ####################################
class PromotionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'promotions/promotions_detail_page.html'
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
    model = Promotion
    form_class = PromotionProductForm
    template_name = 'promotions/promotions_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 1
        
        related_products = self.get_object().promotion_products.values_list('product', flat=True)
        available_products = Product.objects.filter(id__in=related_products)
        context['products_selected'] = available_products
        
        return context

    def form_valid(self, form):
        promotion = form.instance
        promotion.type_prom = form.cleaned_data.get('type_discount')
        promotion.start_date = form.cleaned_data.get('start_date')
        promotion.end_date = form.cleaned_data.get('end_date')

        selected_products = form.cleaned_data['productsSelected']
        existing_products = promotion.promotion_products.all()

        # Elimina las relaciones existentes que ya no están seleccionadas
        for product_relation in existing_products:
            if product_relation.product not in selected_products:
                product_relation.delete()

        # Crea nuevas relaciones solo para productos que no estén asociados actualmente
        for product in selected_products:
            if not promotion.promotion_products.filter(product=product).exists():
                PromotionProduct.objects.create(promotion=promotion, product=product)

        # Guarda la promoción actualizada
        promotion.save()

        return HttpResponseRedirect(reverse_lazy('promotions_app:promotion_detail', kwargs = {'pk':promotion.pk}))

    
#################################### LIST ####################################
class PromotionListView(LoginRequiredMixin, ListView):
    model = Promotion
    template_name = 'promotions/promotions_list_page.html'
    context_object_name = 'promotions'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_column'] = obtener_nombres_de_campos(Promotion, 'description', 'branch', 'discount', 'id', 'created_at', 'deleted_at', 'updated_at', 'user_made')
        return context

    def get_queryset(self):
        
        branch_actualy = set_branch_session(self.request)

        return Promotion.objects.filter(branch=branch_actualy)



# def ajax_promotional_products(request):
#     branch = request.user.branch

#################################### DELETE ####################################
class PromotionDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Promotion
    template_name = 'promotions/promotions_delete_page.html'
    success_url = reverse_lazy('promotions_app:promotion_list')
    
    def form_valid(self, form):
        promotion = self.get_object()
        # print(promotion.promotion_products.all())
        for relation in promotion.promotion_products.all():
            relation.delete()
            
        promotion.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())


def ajax_promotional_products(request):
    branch = request.user.branch

    
    branch_actualy = set_branch_session(request)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        
        promotions = Promotion.objects.filter(branch=branch, is_active=True)  # Obtén todas las promociones
        # print("Obtén todas las promociones")
        # print(promotions)
        list_promotion = {}

        for promotion in promotions:
            # Obtén los productos asociados a cada promoción
            associated_products = promotion.promotion_products.values_list('product__id', flat=True)
            list_promotion[f'{promotion.name}-{promotion.type_prom.name}'] = (promotion.type_prom.name, promotion.discount, list(associated_products))
        # print(list_promotion)
        return JsonResponse({'promotions': list_promotion})