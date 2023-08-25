from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.core.views import CustomUserPassesTestMixin
from .models import Note
from .forms import NoteCreateForm

class NoteCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, FormView):
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

        note = Note.objects.create(**note_data)

        # Notificar a los usuarios conectados
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "broadcast",  # Nombre del canal de transmisión (broadcast)
            {
                "type": "notify.object_created",
                "object_data": f"Nueva nota creada: {note.subject}",
            },
        )

        return super().form_valid(form)
