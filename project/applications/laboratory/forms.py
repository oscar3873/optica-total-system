from django import forms
from .models import Left_eye, Right_eye

class Left_eyeForm(forms.ModelForm):
    form_label = 'Ojo Izquierdo'
    class Meta:
        model = Left_eye
        fields = ['esferic', 'cilindric', 'eje']

class Right_eyeForm(forms.ModelForm):
    form_label = 'Ojo Derecho'

    class Meta:
        model = Right_eye
        fields = ['esferic', 'cilindric', 'eje']

class DistanceForm(forms.Form):
    left_eye = Left_eyeForm()
    right_eye = Right_eyeForm()


class LaboratoryForm(forms.Form):
    far = DistanceForm()
    close = DistanceForm()