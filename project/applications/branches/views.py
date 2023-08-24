from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (FormView, DetailView, UpdateView, View, CreateView)

from .models import Branch
from .forms import BranchForm

from applications.core.views import CustomUserPassesTestMixin


# Create your views here.
class BranchCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        branch = form.save(commit=False)  # Crea una instancia del modelo sin guardarla en la base de datos
        branch.user_made = self.request.user  # Asigna el usuario que creó la sucursal
        branch.save()  # Guarda la instancia con el usuario asignado

        return super().form_valid(form)

