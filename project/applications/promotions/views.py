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

            return super().form_valid(form)
        else:
            return self.form_invalid(form)
