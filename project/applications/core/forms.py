from django import forms

from project.settings.base import DATE_NOW

from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name and len(name) < 3:
            raise forms.ValidationError("Ingrese un Nombre válido.")
        return name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name and len(last_name) < 2:
            raise forms.ValidationError("Ingrese un Apellido válido.")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_str = str(phone_number)
        if phone_number and (len(phone_str) < 7):
            raise forms.ValidationError("Ingrese un número de teléfono válido.")
        return phone_number


    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if dni and (len(dni) < 8 or '.' in dni):
            raise forms.ValidationError('Ingrese un DNI válido sin punto de mil (".").')
        return dni

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and len(email) > 100:
            raise forms.ValidationError("El correo electrónico es demasiado largo.")
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date and birth_date > DATE_NOW:
            raise forms.ValidationError("La fecha de nacimiento no puede estar en el futuro.")
        return birth_date