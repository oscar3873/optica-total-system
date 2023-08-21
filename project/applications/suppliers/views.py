from django.urls import reverse_lazy
from django.views.generic import (View, FormView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SupplierForm
# Create your views here.
class SupplierCreateView(LoginRequiredMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)