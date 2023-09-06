from typing import Any, Dict
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DetailView, ListView

from applications.core.mixins import CustomUserPassesTestMixin # Para Autenticar usuario administrador

from .forms import *
from .models import *
from .utils import *
# Create your views here.

class CategoryCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una catogoria nueva para el producto
    """
    form_class = CategoryForm
    template_name = 'products/category_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user_made = self.request.user
        category.save()
        return super().form_valid(form)


class BrandCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una marca nueva para los productos
    """
    form_class = BrandForm
    template_name = 'products/brand_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.user_made = self.request.user
        brand.save()
        return super().form_valid(form)

class FeatureCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una característica nueva para el producto
    Previa carga del Tipo de Característica
    """
    form_class = FeatureForm
    template_name = 'products/feature_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['type_form'] = FeatureTypeForm()
        return context

    def form_valid(self, form):
        feature = form.save(commit=False)
        feature.user_made = self.request.user
        feature.save()

        for product in form.cleaned_data['products']:
            Product_feature.objects.create(feature=feature, product=product, user_made=self.request.user)

        return super().form_valid(form)


class FeatureTypeCreateView(CustomUserPassesTestMixin, FormView): # TIPO DE CARACTERISTICA (1)
    """
    Crear un tipo para la caracteristica nueva para el producto
        Es lo primero que se crea, luego se crea la caracteristica (tipo -> caracteristica)
    """
    form_class = FeatureTypeForm
    template_name = 'products/featureType_create_page.html'
    success_url = reverse_lazy('products_app:new_feature')

    def form_valid(self, form):
        feature_type = form.save(commit=False)
        feature_type.user_made = self.request.user
        feature_type.save()
                
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
            new_type_data = {
                'id': feature_type.id,
                'name': feature_type.name
            }
            # Si es una solicitud AJAX, devuelve una respuesta JSON
            return JsonResponse({'status': 'success', 'new_type': new_type_data})
        else:
            # Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado
            return super().form_valid(form)


class ProductCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear o actualizar un producto
    """
    form_class = ProductForm
    template_name = 'products/product_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['named_formsets'] = FeatureFormSet(prefix='variants')
        return context

    @transaction.atomic
    def form_valid(self, form):
        # Si es un nuevo producto, simplemente guarda el formulario
        product = form.save(commit=False)
        product.user_made = self.request.user
        product.save()

        feature_formset = FeatureFormSet(self.request.POST, prefix='variants')
        form_in_out_features(form, product, self.request.user)
        if feature_formset.is_valid():
            form_create_features_formset(self.request.user, product, feature_formset)

        return super().form_valid(form)
    
####################### UPDATES #####################

class ProductUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Crear o actualizar un producto
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['named_formsets'] = FeatureFormSet(prefix='variants')
        return context

    @transaction.atomic
    def form_valid(self, form):
        # Si es un nuevo producto, simplemente guarda el formulario
        product = form.instance
        product.user_made = self.request.user

        feature_formset = FeatureFormSet(self.request.POST, prefix='variants')
        form_in_out_features(form, product, self.request.user)
        if feature_formset.is_valid():
            form_create_features_formset(self.request.user, product, feature_formset)

        return super().form_valid(form)

class CategoryUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class BrandUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class FeatureUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Feature
    form_class = FeatureForm
    template_name = 'products/feature_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class FeatureTypeUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Feature_type
    form_class = FeatureForm
    template_name = 'products/featureType_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

################## LIST ######################

class ProductListView(CustomUserPassesTestMixin, ListView):
    model = Product
    template_name = 'products/product_list_page.html'
    context_object_name = 'products'


class BrandListView(CustomUserPassesTestMixin, ListView):
    model = Brand
    template_name = 'products/brand_list_page.html'
    context_object_name = 'brands'


class CategoryListView(CustomUserPassesTestMixin, ListView):
    model = Category
    template_name = 'products/category_list_page.html'
    context_object_name = 'categories'


#################### DETAILS #####################

class ProductDetailView(CustomUserPassesTestMixin, DetailView):
    model = Product
    template_name = 'products/product_page.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.model.objects.get_features(self.get_object())
        return context


#################### FORMULARIO WIZARD #####################
class ProductFormComplete(CustomUserPassesTestMixin, FormView):
    form_class = ProductForm
    template_name = 'products/components/create/product_wizard_form.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryForm
        context['brand_form'] = BrandForm
        context['named_formsets'] = FeatureFormSet(prefix='variants')
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.user_made = self.request.user
            product.save()
        else:
            print('PRODUCTO_FORM_ERRORS: ',form.errors)

        category_form = Category(self.request.POST)
        brand_form = Brand(self.request.POST)
        feature_formset = FeatureFormSet(self.request.POST, prefix='variants')

        form_in_out_features(form, product, self.request.user) # Para el feature_formset
        if feature_formset.is_valid():
            form_create_features_formset(self.request.user, product, feature_formset)
        else:
            print('CARACTERISTICAS_FORM_ERRORS: ',feature_formset.errors)
        
        if category_form.is_valid():
            category_form.save(commit=False)
            category_form.user_made = self.request.user
            category_form.save()
        else:
            print('CATEGORIA_FORM_ERRORS: ',category_form.errors)
        
        if brand_form.is_valid():
            brand_form.save(commit=False)
            brand_form.user_made = self.request.user
            brand_form.save()
        else:
            print('MARCA_FORM_ERRORS: ',brand_form.errors)

        return super().form_valid(form)
