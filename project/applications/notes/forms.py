from django import forms

from .models import Note

class NoteCreateForm(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['user_made',] 
