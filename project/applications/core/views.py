from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView, ListView, DetailView, DeleteView
from django.db import transaction

from applications.core.mixins import CustomUserPassesTestMixin
from applications.cashregister.utils import obtener_nombres_de_campos
from .models import Objetives
from .forms import ObjetiveForm

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"


class ObjetiveCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ObjetiveForm
    template_name = 'core/objetive_page.html'
    success_url = reverse_lazy('core_app:objetive_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 0 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            from applications.branches.utils import set_branch_session
            branch_actualy = set_branch_session(self.request)
            
            # tipo = form.cleaned_data.pop('tipo')
            objetive = form.save(commit=False)
            objetive.branch = branch_actualy
            objetive.user_made = self.request.user
            objetive.save()

        return super().form_valid(form)


class ObjetiveUpdateView(CustomUserPassesTestMixin, UpdateView):
    form_class = ObjetiveForm
    model = Objetives
    template_name = 'core/objetive_page.html'
    success_url = reverse_lazy('core_app:objetive_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 1 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context
    

class ObjetivesListView(ListView):
    model = Objetives
    template_name = 'core/objetives_view.html'
    paginator = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['table_column'] = obtener_nombres_de_campos(Objetives,
            "id",
            "deleted_at", 
            "created_at", 
            "updated_at",
            "branch",
            )
        return context
    
class ObjetiveDetail(DetailView):
    model = Objetives
    template_name = 'core/objetives_detail.html'


class ObjetiveDelete(DeleteView):
    model = Objetives
    template_name = 'core/objetive_delete_page.html'
    context_object_name = 'objetive'

    def form_valid(self, form):
        objetive = self.get_object()
        print('\n\n\n', objetive)
        to = objetive.to_branch.all() or objetive.to_employees.all()
        for un in to:
            un.delete()

        return HttpResponseRedirect(reverse_lazy('core_app:objetive_list'))
