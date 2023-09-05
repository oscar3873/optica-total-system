from .models import Note, Branch
from django import forms
from applications.core.mixins import ValidationFormMixin


class NoteCreateForm(ValidationFormMixin):
    """
    Formulario para ingresar una nueva nota
        fields: [subject,description,branch]
    """
    branches = Branch.objects.all()
    branch_choices = [(0,'Seleccione una sucursal')]
    branch_choices += [(branch.id,branch.name) for branch in branches]

    subject = forms.CharField(
        label = 'Asunto',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    description = forms.CharField(
        label = 'Descripcion',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': '5',
                   }
        ),
    )
    
    branch = forms.ModelChoiceField(
        label='Sucursal',
        queryset=Branch.objects.all(),  # Queryset con todas las sucursales
        empty_label='Seleccione una sucursal',  # Etiqueta para la opción vacía
        widget=forms.Select(
            attrs={
                'class': 'form-select'
                }
        ),
    )

    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['user_made',]

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        self.validate_length(subject, 3, 'El título debe tener al menos 3 caracteres.')
        return subject
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        self.validate_length(description,5,'El contenido del mensaje debe ser de al menos 5 caracteres.')
        return description
    

    def clean_branch(self):
        branch = self.cleaned_data.get('branch')
        if branch is None:
            raise forms.ValidationError('Debe seleccionar una sucursal')
        return branch