from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DetailView, ListView

from applications.core.mixins import CustomUserPassesTestMixin # Para Autenticar usuario administrador

from .forms import *
from .models import *
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

class FeatureCreateView(CustomUserPassesTestMixin, FormView): # CARACTERISTICA Y SU TIPO (2)
    """
    Crear una caracteristica nueva para el producto
        Previa carga del Tipo de Caracteristica
    """
    form_class = FeatureForm
    template_name = 'products/feature_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        feature = form.save(commit=False)
        feature.user_made = self.request.user
        feature = Feature.objects.create(**feature)

        for product in form.cleaned_data['products']:
            Product_feature.objects.create(feature=feature, product=product, user_made = self.request.user)

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
        Feature_type.objects.create(**feature_type)
        return super().form_valid(form)


class ProductCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear o actualizar un producto
    """
    form_class = ProductForm
    template_name = 'products/product_create_page.html'
    success_url = reverse_lazy('core_app:home')
    create_mode = True  # Indica si estamos en modo de creación o actualización

    def dispatch(self, request, *args, **kwargs):
        # Verificar si estamos en modo de actualización
        if 'pk' in self.kwargs:
            self.create_mode = False
            self.object = Product.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.create_mode:
            context['form'] = ProductForm(instance = self.object)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        """
        Funcion para obtener el formulario formset para GET y POST
        """
        if self.request.method == "GET":
            return FeatureFormSet(prefix='variants')
        else:
            return FeatureFormSet(self.request.POST, prefix='variants')

    @transaction.atomic
    def form_valid(self, form):
        if not self.create_mode:
            # Actualiza los campos del objeto con los datos del formulario POST
            form.instance.pk = self.object.pk  # Mantén la clave primaria
            form.instance.user_made = self.request.user  # Actualiza el usuario
            product = form.save()  # Guarda los cambios en el objeto existente
        else:
            # Si es un nuevo producto, simplemente guarda el formulario
            product = form.save(commit=False)
            product.user_made = self.request.user
            product.save()

        feature_formset = self.get_named_formsets()
        if feature_formset.is_valid():
            Product_feature.objects.form_in_out_features(form, product, self.request.user)
            Product_feature.objects.form_create_features_formset(product, feature_formset)

        return super().form_valid(form)
    
####################### UPDATES #####################

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
