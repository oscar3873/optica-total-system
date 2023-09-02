from django.urls import reverse_lazy
from django.views.generic import (FormView, DetailView, UpdateView, View)

from .forms import BranchForm

from applications.core.mixins import CustomUserPassesTestMixin


# Create your views here.
class BranchCreateView(CustomUserPassesTestMixin, FormView):
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.user_made = self.request.user
        branch.save()
        return super().form_valid(form)

