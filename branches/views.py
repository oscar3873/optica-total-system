from django.http import HttpResponseRedirect

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (FormView, DetailView, UpdateView, DeleteView, ListView, View) #aqui
from django.contrib import messages
from .forms import BranchForm
from .models import Branch, Branch_Objetives

from core.mixins import CustomUserPassesTestMixin, LoginRequiredMixin


# Create your views here.

####################### CREATE #####################
class BranchCreateView(CustomUserPassesTestMixin, FormView):
    """
    Crear una nueva sucursal
    """
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        if self.request.user.is_staff:
            self.success_url = reverse_lazy('dashboard_app:daily_summary') 
        else:
            self.success_url = reverse_lazy('sales_app:point_of_sale_view')
        branch = form.save(commit=False)
        branch.user_made = self.request.user
        branch.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)


####################### UPDATES #####################

class BranchUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/branch_update.html'
    success_url = reverse_lazy('branches_app:branch_list')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

####################### DETAILS #####################

class BranchDetailView(CustomUserPassesTestMixin, DetailView):
    model = Branch
    template_name = 'branches/branch_detail.html'
    context_object_name = 'branch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch_pk = self.kwargs['pk']
        context['objectives'] = Branch_Objetives.objects.filter(branch_id=branch_pk)
        #context['features'] = self.model.objects.get_features(self.get_object())
        return context

    def get_object(self, queryset=None):
        # Obtener el objeto Branch basado en el pk proporcionado en la URL
        pk = self.kwargs.get('pk')
        return Branch.objects.get(pk=pk)

####################### DELETE #####################

class BranchDeleteView(LoginRequiredMixin, DeleteView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave

        if self.request.user.is_staff:
            self.success_url = reverse_lazy('dashboard_app:daily_summary') 
        else:
            self.success_url = reverse_lazy('sales_app:point_of_sale_view')

        return HttpResponseRedirect(self.get_success_url())


################## LIST ######################

class BranchListView(CustomUserPassesTestMixin, ListView):
    model = Branch
    template_name = 'branches/branch_list.html'
    context_object_name = 'branches'
    paginate_by = 8


class BranchChangeView(View):
    template_name = 'cambiar_sucursal.html'  # Nombre del template HTML

    def get(self, request):
        # Recupera todas las sucursales disponibles para el administrador
        branches = Branch.objects.all()

        return render(request, self.template_name, {'branches': branches})
    
    def post(self, request):
        sucursal_id = request.POST.get('branch_id')
        if sucursal_id:
            request.session['branch_actualy'] = int(sucursal_id)
        # Redirige de vuelta a la página desde la que se hizo el cambio
        if request.user.is_staff:
            url = reverse_lazy('dashboard_app:daily_summary') 
        else:
            url = reverse_lazy('sales_app:point_of_sale_view')
        return redirect(request.META.get('HTTP_REFERER', url))