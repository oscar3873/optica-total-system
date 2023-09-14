from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (FormView, DetailView, UpdateView, DeleteView, ListView) #aqui

from .forms import BranchForm
from .models import Branch

from applications.core.mixins import CustomUserPassesTestMixin, LoginRequiredMixin


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
        branch = form.save(commit=False)
        branch.user_made = self.request.user
        branch.save()
        return super().form_valid(form)


####################### UPDATES #####################

class BranchUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/branch_update.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)

####################### DETAILS #####################

class BranchDetailView(CustomUserPassesTestMixin, DetailView):
    model = Branch
    template_name = 'branches/branch_form.html'
    context_object_name = 'Branch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.model.objects.get_features(self.get_object())
        return context

####################### DELETE #####################

class BranchDeleteView(LoginRequiredMixin, DeleteView):
    model = Branch
    form_class = BranchForm
    template_name = 'branches/branch_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())


################## LIST ######################

class BranchListView(CustomUserPassesTestMixin, ListView):
    model = Branch
    template_name = 'branches/branch_list.html'
    context_object_name = 'branches'
    paginate_by = 8