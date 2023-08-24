from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.core.views import CustomUserPassesTestMixin
from .forms import NoteCreateForm

class NoteCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, FormView):
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user_made = self.request.user
        note.save()

        # Notificar a los usuarios conectados
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "broadcast",  # Nombre del canal de transmisión (broadcast)
            {
                "type": "notify.object_created",
                "object_data": f"Nueva nota creada: {note.titulo}",
            },
        )

        return super().form_valid(form)
