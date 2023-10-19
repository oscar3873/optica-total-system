from django.http import JsonResponse
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from applications.core.mixins import CustomUserPassesTestMixin
from .models import *
from .forms import *

# Create your views here.
class PromotionCreateView(CustomUserPassesTestMixin, FormView):
    form_class = PromotionFormSet
    template_name = 'promotions/promotions_page.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        formset = PromotionFormSet(self.request.POST)
        if formset.is_valid():
            # Procesar los formularios del formset
            for extra_form in formset:
                if extra_form.is_valid():
                    print('FORMSET UNIT',extra_form.cleaned_data)
                    promotion = extra_form.save(commit=False)
                    if promotion.name: # En teoria si tiene name, description, start_date, end_date es porque el formulario es el original (form-0)
                        name = promotion.name
                        description = promotion.description
                        start_date = promotion.start_date
                        end_date = promotion.end_date
                    else:
                        promotion.name = name
                        promotion.description = description
                        promotion.start_date = start_date
                        promotion.end_date = end_date
                    print(promotion)
                    # promotion.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PromotionDetailView(TemplateView):
    template_name = 'promotions/promotions_detail_page.html'


def ajax_promotional_products(request):
    branch = request.user.branch

    branch_actualy = request.session.get('branch_actualy')
    if request.user.is_staff and branch_actualy:
        branch = Branch.objects.get(id=branch_actualy)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        list_promotion = { # Lista de promociones con sus respectivos productos asociados
            'A' : ['1', '2', '3'], # 2x1
            'B' : ['4', '5'],      # 50% off
            'C' : [''],            # descuento %
        }
        # Crear una lista de diccionarios con los datos de los empleados
        return JsonResponse({'promotions': list_promotion})