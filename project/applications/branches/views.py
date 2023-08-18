from typing import Optional
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (CreateView, DetailView, UpdateView, View)

from .models import Branch
from .forms import BranchForm

# Create your views here.
class BranchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/new_branch.html'
    success_url = reverse_lazy('core_app:home')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super(LoginRequiredMixin, self).handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)
