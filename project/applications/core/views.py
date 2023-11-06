from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView

from applications.core.mixins import CustomUserPassesTestMixin
from applications.branches.models import Branch, Branch_Objetives
from applications.employes.models import Employee, Employee_Objetives
from .forms import ObjetiveForm

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"

class ObjetiveCreateView(CustomUserPassesTestMixin, FormView):
    form_class = ObjetiveForm
    template_name = 'core/objetive_page.html'

    def form_valid(self, form):
        if form.is_valid():
            tipo = form.cleaned_data.pop('tipo')
            # objetive = form.save(commit=False)
            objetive = form.save()
            
            branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
            branch_actualy = Branch.objects.get(id=branch_actualy)

            employees = Employee.objects.filter(branch=branch_actualy)
            branches = Branch.objects.all()

            if 'EMPLEADOS' in objetive.to:
                for employee in employees:
                    Employee_Objetives.objects.create(
                        employee = employee,
                        objetive = objetive,
                    )
            elif 'SUCURSAL' in objetive.to:
                for branch in branches:
                    Branch_Objetives.objects.create(
                        branch = branch,
                        objetive = objetive,
                    )

        return super().form_valid(form)
