from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, UpdateView

from applications.core.mixins import CustomUserPassesTestMixin
from applications.branches.models import Branch
from .models import Objetives
from .forms import ObjetiveForm

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"

class ObjetiveCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ObjetiveForm
    template_name = 'core/objetive_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 0 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context

    def form_valid(self, form):
        if form.is_valid():
            branch_actualy = Branch.objects.get(id=branch_actualy)
            branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
            
            tipo = form.cleaned_data.pop('tipo')
            objetive = form.save(commit=False)
            objetive.branch = branch_actualy
            objetive.save()

        return super().form_valid(form)

class ObjetiveUpdateView(CustomUserPassesTestMixin, UpdateView):
    form_class = ObjetiveForm
    model = Objetives
    template_name = 'core/objetive_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 1 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context