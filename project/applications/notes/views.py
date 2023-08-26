from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.core.mixins import CustomUserPassesTestMixin
from .models import Note
from .forms import NoteCreateForm

class NoteCreateView(CustomUserPassesTestMixin, FormView):
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        note_data = {
            'user_made': self.request.user,
            'subject': form.cleaned_data['subject'],
            'description': form.cleaned_data['description'],
            'branch': form.cleaned_data['branch'],
        }
        Note.objects.create(**note_data)
        return super().form_valid(form)
