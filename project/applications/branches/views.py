from typing import Optional
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (FormView, DetailView, UpdateView, View, CreateView)

from .models import Branch
from .forms import BranchForm

from applications.core.views import CustomUserPassesTestMixin


# Create your views here.
class BranchCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, FormView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/brand_form.html'
    success_url = reverse_lazy('core_app:home')
