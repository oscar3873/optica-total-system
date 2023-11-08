from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView
from django.db import transaction

from applications.core.mixins import CustomUserPassesTestMixin
from .models import Objetives
from .forms import ObjetiveForm

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"


class ObjetiveCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ObjetiveForm
    template_name = 'core/objetive_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 0 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            from applications.branches.utils import set_branch_session
            branch_actualy = set_branch_session(self.request)
            
            tipo = form.cleaned_data.pop('tipo')
            objetive = form.save(commit=False)
            objetive.branch = branch_actualy
            objetive.user_made = self.request.user
            objetive.save()

        return super().form_valid(form)


class ObjetiveUpdateView(CustomUserPassesTestMixin, UpdateView):
    form_class = ObjetiveForm
    model = Objetives
    template_name = 'core/objetive_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 1 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context