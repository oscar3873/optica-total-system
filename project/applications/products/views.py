from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.core.views import CustomUserPassesTestMixin #Para Autenticar usuario administrador

from .forms import BrandForm, CategoryForm, ProductForm
# Create your views here.

class CategoryCreateView(LoginRequiredMixin, FormView):
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

class BrandCreateView(LoginRequiredMixin, FormView):
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

class ProductCreateView(LoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('core_app:home')