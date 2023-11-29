from typing import Any
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView, ListView, DetailView, DeleteView
from django.db import transaction

from core.mixins import CustomUserPassesTestMixin
from cashregister.utils import obtener_nombres_de_campos
from .models import Objetives
from .forms import ObjetiveForm

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"
    success_url = reverse_lazy('sales_app:point_of_sale_view')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                self.success_url = reverse_lazy('dashboard_app:daily_summary') 
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class ObjetiveCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ObjetiveForm
    template_name = 'core/objetive_page.html'
    success_url = reverse_lazy('core_app:objetive_list')
    context_object_name = 'objetive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 0 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            from branches.utils import set_branch_session
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
    context_object_name = 'objetive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = 1 # Para reutilizar el mismo template pero con el texto que corresponda al formulario (actaulizar o crear)
        return context
    

class ObjetivesListView(ListView):
    model = Objetives
    template_name = 'core/objetives_view.html'
    paginator = 5
    context_object_name = 'objetives'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['table_column'] = obtener_nombres_de_campos(Objetives,
            "id",
            "user_made",
            "deleted_at", 
            "created_at", 
            "updated_at",
            "branch",
            )
        return context
    
class ObjetiveDetail(DetailView):
    model = Objetives
    template_name = 'core/objetive_detail_page.html'
    context_object_name = 'objetive'


class ObjetiveDelete(DeleteView):
    model = Objetives
    template_name = 'core/objetive_delete_page.html'
    context_object_name = 'objetive'

    def form_valid(self, form):
        objetive = self.get_object()
        to = objetive.to_branch.all() or objetive.to_employees.all()
        for un in to:
            un.delete()
        objetive.delete()

        return HttpResponseRedirect(reverse_lazy('core_app:objetive_list'))
