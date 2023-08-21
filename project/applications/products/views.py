from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.core.views import CustomUserPassesTestMixin # Para Autenticar usuario administrador

from .forms import *
from .models import *
# Create your views here.

class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

class BrandCreateView(LoginRequiredMixin, CreateView):
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('core_app:home')

class FeatureCreateView(LoginRequiredMixin, CreateView): # CARACTERISTICA Y SU TIPO (2)
    form_class = FeatureForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

class FeatureTypeCreateView(LoginRequiredMixin, CreateView): # TIPO DE CARACTERISTICA (1)
    form_class = FeatureTypeForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products_app:new_feature')


####################### UPDATES #####################

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('core_app:home')

class FeatureUpdateView(LoginRequiredMixin, UpdateView):
    model = Feature
    form_class = FeatureForm
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

class FeatureTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Feature_type
    form_class = FeatureForm
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

################## LIST ######################

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # Reemplaza con la plantilla adecuada
    context_object_name = 'products'  # Nombre de la variable en el contexto

    def get_queryset(self):
        return Product.objects.all()