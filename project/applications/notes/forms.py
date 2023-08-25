from django import forms

from .models import Note

################################################################
def validate_length(field_value, min_length, error_message):
    """
    Valida longitud de una cadena.
        Para nombres, apellidos, direcciones, telefonos, etc.
        Muestra el error mandado por argumento.
    """
    if field_value and len(field_value) < min_length:
        raise forms.ValidationError(error_message)
################################################################

class NoteCreateForm(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['user_made',] 

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        validate_length(subject, 3, 'El título debe tener al menos 3 carácteres.')
        return subject