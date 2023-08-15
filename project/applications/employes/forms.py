from django import forms
from .models import Employee
from applications.core.forms import PersonForm

class EmployeeCreateForm(PersonForm):
    class Meta:
        model = Employee
        fields = ['from_branch',]