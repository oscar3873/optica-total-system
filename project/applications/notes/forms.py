from .models import Note, Branch, Label
from django import forms
from applications.core.mixins import ValidationFormMixin

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'

class LabelCreateForm(ValidationFormMixin):
    
    label = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'Ej: Recordatorio'}
        )
    )

    color = forms.CharField(
        widget=ColorPickerWidget(
            attrs={'class': 'form-control form-control-color'}
        )
    )

    class Meta:
        model = Label
        fields = ['label','color']

    def clean_label(self):
        label = self.cleaned_data.get('label')
        self.validate_length(label, 3, 'Debe contener por lo menos 3 caracteres.')
        return label.upper() 

class NoteCreateForm(ValidationFormMixin):
    """
    Formulario para ingresar una nueva nota
    fields: [subject, description, branch]
    """

    subject = forms.CharField(
        label='Asunto',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'Ej: Cumpleaños de Juan'}
        )
    )

    description = forms.CharField(
        label='Descripcion',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 
                'placeholder': 'Ej: Felicidades Juan!!',
                'rows': '5'}
        ),
    )

    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        label='Tipo de Nota',
        empty_label='Elija un tipo',
        required=True,
        widget=forms.Select(attrs={
            'placeholder': 'Sucursal',
            'class': 'form-control'
        })
    )

    color_value = forms.CharField(
    )

    class Meta:
        model = Note
        fields = ['subject', 'description', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            print(self.instance.label.color)
            self.fields['color_value'].initial = self.instance.label.color


    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        self.validate_length(subject, 3, 'El título debe tener al menos 3 caracteres.')
        return subject.title()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        self.validate_length(description, 5, 'El contenido del mensaje debe ser de al menos 5 caracteres.')
        return description.title()

    def clean_label(self):
        label = self.cleaned_data.get('label')
        if label is None:
            raise forms.ValidationError('Debe seleccionar el tipo de nota')
        return label