from django import forms

from .models import Laboratory

class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = '__all__'