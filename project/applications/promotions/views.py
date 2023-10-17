from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages

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
