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
        category_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
        }
        Category.objects.create(**category_data)
        return super().form_valid(form)


class BrandCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una marca nueva para los productos
    """
    form_class = BrandForm
    template_name = 'products/brand_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        brand_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
        }
        Brand.objects.create(**brand_data)
        return super().form_valid(form)

class ProductCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear un producto
    """
    form_class = ProductForm
    template_name = 'products/product_create_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        produtct_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
            'price': form.cleaned_data['price'],
            'description': form.cleaned_data['description'],
            'stock': form.cleaned_data['stock'],
            'category': form.cleaned_data['category'],
            'brand': form.cleaned_data['brand'],
            'barcode': form.cleaned_data['barcode'],
        }
        prouct = Product.objects.create(**produtct_data)

        for feature in form.cleaned_data['features']:
            Product_feature.objects.create(feature=feature, product=prouct, user_made = self.request.user)

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
        feature_data = {
            'user_made': self.request.user,
            'value': form.cleaned_data['value'],
            'type': form.cleaned_data['type'],
        }
        feature = Feature.objects.create(**feature_data)

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
        feature_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
        }
        Feature_type.objects.create(**feature_data)
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

class ProductUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        product = form.save()

        selected_features = form.cleaned_data['features']
        existing_features = product.product_feature.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for feature in existing_features:
            if feature.feature not in selected_features:
                product.product_feature.get(feature=feature.feature).delete()

        # Crea nuevas relaciones solo para características no existentes
        for feature in selected_features:
            if feature not in existing_features.values_list('feature', flat=True):
                Product_feature.objects.create(product=product, feature=feature, user_made= self.request.user)

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
