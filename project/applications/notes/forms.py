from .models import Note, Branch, Label
from django import forms
from applications.core.mixins import ValidationFormMixin


class NoteCreateForm(ValidationFormMixin):
    """
    Formulario para ingresar una nueva nota
        fields: [subject,description,branch]
    """
    # branches = Branch.objects.all()
    # branch_choices = [(0,'Seleccione una sucursal')]
    # branch_choices += [(branch.id,branch.name) for branch in branches]

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

    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        label='Tipo de Nota',
        empty_label='Elija un tipo',
        required=True,
        widget=forms.Select(attrs={
            'placeholder' : 'Sucursal',
            'class' : 'form-control'
        })
    )
    
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        label='Sucursal',
        empty_label='Elija una sucursal',
        required=True,
        widget=forms.Select(attrs={
            'placeholder' : 'Sucursal',
            'class' : 'form-control'
        })
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
    
    def clean_label(self):
        label = self.cleaned_data.get('label')
        if label is None:
            raise forms.ValidationError('Debe seleccionar el tipo de nota')
        return label