from django.urls import reverse_lazy
from django.views.generic import (CreateView, View, FormView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Supplier
from .forms import SupplierForm
# Create your views here.
class SupplierCreateView(LoginRequiredMixin, FormView):
    form_class = SupplierForm
    template_name = 'supplier/new_supplier.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        
        return super().form_valid(form) 