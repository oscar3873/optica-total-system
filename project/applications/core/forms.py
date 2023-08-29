from .models import Person
from .mixins import ValidationFormMixin

class PersonForm(ValidationFormMixin):
    class Meta:
        model = Person
        fields = '__all__'

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        self.validate_length(name, 3, "Ingrese un nombre válido.")
        return name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        self.validate_length(last_name, 3, "Ingrese un apellido válido.")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        self.validate_length(phone_number, 9, "Ingrese un número de teléfono válido")
        return phone_number

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        self.validate_length(dni, 7, "Ingrese un número de DNI válido.")
        return dni

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date