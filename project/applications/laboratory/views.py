from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import LaboratoryForm
# Create your views here.
class LaboratoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = LaboratoryForm
    template_name = 'laboratory/create_form.html'
    success_url = reverse_lazy('core_app:home')

    def test_func(self):
        """
        Para la verificacion de Administrador
        """
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super(LoginRequiredMixin, self).handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)
