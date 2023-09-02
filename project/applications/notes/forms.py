from .models import Note
from applications.core.mixins import ValidationFormMixin


class NoteCreateForm(ValidationFormMixin):
    
    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['user_made',] 

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        self.validate_length(subject, 3, 'El título debe tener al menos 3 carácteres.')
        return subject
