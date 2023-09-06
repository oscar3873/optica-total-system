from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from applications.core.mixins import CustomUserPassesTestMixin
from .consumers import send_global_message
from .models import Note
from .forms import NoteCreateForm

class NoteCreateView(CustomUserPassesTestMixin, FormView):
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        """
        Crea una Nota
        """
        #Creo una nueva instancia de Nota y asigno sucursal
        note = form.save(commit=False)
        note.branch = form.cleaned_data['branch']
        note.user_made = self.request.user
        note.save()
        
        #Comento esta seccion, me da error  -> Error 111 connecting to 127.0.0.1:6379. 111.
        # Send a global message using the send_global_message function
        # send_global_message(f"A new note has been created: {note.subject}")

        return super().form_valid(form)


################## LIST ######################

class NoteListView(CustomUserPassesTestMixin, ListView):
    model = Note
    template_name = 'notes/notes_page.html'
    context_object_name = 'notes'
    paginate_by = 4