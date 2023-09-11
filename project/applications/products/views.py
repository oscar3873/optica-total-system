from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DetailView, ListView, DeleteView
from django.contrib import messages

from applications.core.mixins import CustomUserPassesTestMixin # Para Autenticar usuario administrador

from .forms import *
from .models import *
from .utils import *
# Create your views here.

class CategoryCreateView(FormView):
    """
    Crear una catogoria nueva para el producto
    """
    form_class = CategoryForm
    template_name = 'products/category_create_page.html'
    success_url = reverse_lazy('products_app:category_list')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user_made = self.request.user
        category.save()

        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
            new_category_data = {
                'id': category.id,
                'name': category.name
            }
            # Si es una solicitud AJAX, devuelve una respuesta JSON
            return JsonResponse({'status': 'success', 'new_category': new_category_data})
        else:
            # Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado
            return super().form_valid(form)

class BrandCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una marca nueva para los productos
    """
    form_class = BrandForm
    template_name = 'products/brand_create_page.html'
    success_url = reverse_lazy('products_app:brand_list')

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.user_made = self.request.user
        brand.save()

        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
            new_brand_data = {
                'id': brand.id,
                'name': brand.name
            }
            # Si es una solicitud AJAX, devuelve una respuesta JSON
            return JsonResponse({'status': 'success', 'new_brand': new_brand_data})
        else:
            # Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado
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


#################### FORMULARIO WIZARD #####################
class ProductCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ProductForm
    template_name = 'products/components/create/product_wizard_form.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['named_formsets'] = FeatureFormSet(prefix='variants')
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.user_made = self.request.user
            product.save()
            form_in_out_features(form, product, self.request.user)

        feature_formset = FeatureFormSet(self.request.POST, prefix='variants')

        if feature_formset.is_valid():
            form_create_features_formset(self.request.user, product, feature_formset)
    
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)
    
    
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
        context['brand_form']=BrandForm()
        context['category_form']=CategoryForm()
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
        category = form.save(commit=False)
        category.user_made = self.request.user
        category.save()
                
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
    def get_queryset(self):
        branch = self.request.user.branch #recupero el brach del user
        if branch == None:
            return Product.objects.filter(deleted_at=None)
        else:
            # Filtra los productos que no han sido eliminados suavemente
            return Product.objects.filter(deleted_at=None,branch=branch)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.request.user.branch
        try:
            products = Product.objects.filter(branch=branch, deleted_at=None)
        except Product.DoesNotExist:
            products = None
        context['products'] = products
        
        exclude_fields = ["id", "deleted_at", "created_at", "updated_at"]
        context['table_column'] = obtener_nombres_de_campos(Product, *exclude_fields)
        
        return context


class BrandListView(CustomUserPassesTestMixin, ListView):
    model = Brand
    template_name = 'products/brand_list_page.html'
    context_object_name = 'brands'
    def get_queryset(self):
        # Filtra los productos que no han sido eliminados suavemente
        return Brand.objects.filter(deleted_at=None)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_column'] = obtener_nombres_de_campos(Brand,"id","deleted_at", "created_at", "updated_at")
        return context

class CategoryListView(CustomUserPassesTestMixin, ListView):
    model = Category
    template_name = 'products/category_list_page.html'
    context_object_name = 'categories'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_column'] = obtener_nombres_de_campos(Category,"id","deleted_at", "created_at", "updated_at")
        return context

#################### DETAILS #####################

class ProductDetailView(CustomUserPassesTestMixin, DetailView):
    model = Product
    template_name = 'products/product_page.html'
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.request.user.branch
        
        if not self.object.branch == branch: # Valida que el usuario no pueda entrar por URL (product/<pk>/)
            messages.error(self.request, 'Lo sentimos, no puedes ver este producto.')
        
        context['features'] = self.model.objects.get_features(self.get_object())
        return context
    
    
class CategoryDetailView(CustomUserPassesTestMixin, DetailView):
    model = Category
    template_name = 'products/category_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = Product.objects.filter(category=self.object, deleted_at=None)
        # AGREGAR MAS DETALLES RELACIONADOS
        return context


class BrandDetailView(CustomUserPassesTestMixin, DetailView):
    model = Brand
    template_name = 'products/brand_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = Product.objects.filter(brand=self.object, deleted_at=None)
        # AGREGAR MAS DETALLES RELACIONADOS
        return context
    


########################### DELETE ####################################

class CategoryDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'products/category_delete_page.html'
    success_url = reverse_lazy('products_app:category_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())

class BrandDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Brand
    template_name = 'products/brand_delete_page.html'
    success_url = reverse_lazy('products_app:brand_list')
    

class ProductDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete_page.html'
    success_url = reverse_lazy('products_app:product_list')


class FeatureDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Feature
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('core_app:home')
    

class FeatureTypeDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Feature_type
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products_app:new_feature')
    