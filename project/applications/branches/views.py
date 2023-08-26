from django.urls import reverse_lazy
from django.views.generic import (FormView, DetailView, UpdateView, View)

from .models import Branch
from .forms import BranchForm

from applications.core.views import CustomUserPassesTestMixin


# Create your views here.
class BranchCreateView(CustomUserPassesTestMixin, FormView):
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        branch_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
            'address': form.cleaned_data['address'],
            'open_hs': form.cleaned_data['open_hs'],
            'close_hs': form.cleaned_data['close_hs'],
        }
        Branch.objects.create(**branch_data)
        return super().form_valid(form)

