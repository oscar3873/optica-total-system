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
    template_name = 'products/category_form.html'
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
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.user_made = self.request.user
        brand.save()
        return super().form_valid(form)


from django.shortcuts import get_object_or_404

class ProductCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear o actualizar un producto
    """
    form_class = ProductForm
    template_name = 'products/product_form.html'
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
        if self.request.method == "GET":
            return {'variants': FeatureFormSet(prefix='variants')}
        else:
            return {'variants': FeatureFormSet(self.request.POST, prefix='variants')}

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

        feature_formset = self.get_named_formsets()['variants']
        if feature_formset.is_valid():
            feature_dict = {}
            # Guardar o actualizar el producto según el modo
            # if not self.create_mode:
            selected_features = form.cleaned_data['features']
            existing_features = product.product_feature.all()

            # Elimina relaciones existentes que ya no están seleccionadas
            for feature in existing_features:
                if feature.feature not in selected_features:
                    product.product_feature.get(feature=feature.feature).delete()

            # Crea nuevas relaciones solo para características no existentes
            for feature in selected_features:
                if feature not in existing_features.values_list('feature', flat=True):
                    prueba = Product_feature.objects.create(product=product, feature=feature, user_made= self.request.user)


            for feature_form in feature_formset:
                feature_type_name = feature_form.cleaned_data.get('type', '').strip().lower()
                feature_value = feature_form.cleaned_data.get('value', '').strip().lower()
                if feature_type_name and feature_value:
                    # Create FeatureType if it doesn't exist
                    feature_type, created = Feature_type.objects.get_or_create(
                                                user_made=self.request.user,
                                                name=feature_type_name)
                    value, created = Feature.objects.get_or_create(
                                        user_made=self.request.user,
                                        type=feature_type,
                                        value=feature_value
                                    )
                    feature_dict[value] = feature_type

            for feature, feature_type_name in feature_dict.items():
                intermedia, created = Product_feature.objects.get_or_create(
                    product=product,
                    feature=feature
                )
                print(intermedia == prueba, created)

        return super().form_valid(form)


class FeatureCreateView(CustomUserPassesTestMixin, FormView): # CARACTERISTICA Y SU TIPO (2)
    """
    Crear una caracteristica nueva para el producto
        Previa carga del Tipo de Caracteristica
    """
    form_class = FeatureForm
    template_name = 'products/category_form.html'
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
    template_name = 'products/category_form.html'
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
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class BrandUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class ProductUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
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
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

class FeatureTypeUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Feature_type
    form_class = FeatureForm
    template_name = 'products/feature_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

################## LIST ######################

class ProductListView(CustomUserPassesTestMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class BrandListView(CustomUserPassesTestMixin, ListView):
    model = Brand
    template_name = 'products/brand_list.html'
    context_object_name = 'brands'


class CategoryListView(CustomUserPassesTestMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


#################### DETAILS #####################

class ProductDetailView(CustomUserPassesTestMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.model.objects.get_features(self.get_object())
        return context
