from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.core.views import CustomUserPassesTestMixin # Para Autenticar usuario administrador

from .forms import *
from .models import *
# Create your views here.

class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Crear una catogoria nueva para el producto
    """
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)


class BrandCreateView(LoginRequiredMixin, CreateView):
    """
    Crear una marca nueva para los productos
    """
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Crear unun producto
    """
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class FeatureCreateView(LoginRequiredMixin, CreateView): # CARACTERISTICA Y SU TIPO (2)
    """
    Crear una caracteristica nueva para el producto
        Previa carga del Tipo de Caracteristica
    """
    form_class = FeatureForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class FeatureTypeCreateView(LoginRequiredMixin, CreateView): # TIPO DE CARACTERISTICA (1)
    """
    Crear un tipo para la caracteristica nueva para el producto
        Es lo primero que se crea, luego se crea la caracteristica (tipo -> caracteristica)
    """
    form_class = FeatureTypeForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products_app:new_feature')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)


####################### UPDATES #####################

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class FeatureUpdateView(LoginRequiredMixin, UpdateView):
    model = Feature
    form_class = FeatureForm
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

class FeatureTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Feature_type
    form_class = FeatureForm
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)

################## LIST ######################

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'  # Reemplaza con la plantilla adecuada
    context_object_name = 'products'  # Nombre de la variable en el contexto


class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'products/brand_list.html'
    context_object_name = 'brands'


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


#################### DETAILS #####################

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.model.objects.get_features(self.get_object())
        return context