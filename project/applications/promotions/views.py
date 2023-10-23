from django.http import HttpResponseRedirect, JsonResponse
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
    form_class = PromotionProductForm
    template_name = 'promotions/promotions_page.html'
    success_url = reverse_lazy('promotions_app:promotion_list')

    def form_valid(self, form):
        print(form.cleaned_data)
        # Crea la promoción sin guardarla en la base de datos aún
        promotion = form.save(commit=False)
        promotion.branch = self.request.user.branch
        promotion.type_prom = form.cleaned_data.get('type_discount')
        # Guarda la promoción en la base de datos
        promotion.save()
        # Obtiene los productos seleccionados del formulario
        selected_products = form.cleaned_data.get('productsSelected')
        print(selected_products)
        for product in selected_products:
            # Crea una relación entre la promoción y el producto
            PromotionProduct.objects.create(promotion=promotion, product=product)
        # Redirige a la página de inicio o a donde desees después de guardar
        return super().form_valid(form)


#################################### DETAILS ####################################
class PromotionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'promotions/promotion_detail_page.html'
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
    template_name = 'promotions/promotion_update_page.html'
    success_url = reverse_lazy('promotions_app:promotion_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar datos adicionales al contexto si es necesario
        return context

    def form_valid(self, form):
        promotion = form.save(commit=False)  # No guardamos inmediatamente
        promotion.save()  # Guarda la promoción actualizada

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

        return super().form_valid(form)


    
#################################### LIST ####################################
class PromotionListView(LoginRequiredMixin, ListView):
    model = Promotion
    template_name = 'promotions/promotions_list_page.html'
    context_object_name = 'promotions'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        promotion_model = Promotion
        custom_fields = [
            field.name for field in promotion_model._meta.get_fields()
            if not field.is_relation
        ]
        context['table_column'] = custom_fields
        return context

    def get_queryset(self):
        user = self.request.user
        branch_actualy = self.request.session.get('branch_actualy')

        if branch_actualy is not None:
            branch_actualy = Branch.objects.get(id=branch_actualy)
            branch = branch_actualy
        else:
            branch = user.branch

        return Promotion.objects.filter(branch=branch)



# def ajax_promotional_products(request):
#     branch = request.user.branch

#################################### DELETE ####################################
class PromotionDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Promotion
    template_name = 'promotions/promotions_delete_page.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())

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