from django.http import HttpResponseRedirect
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

    def get_form_kwargs(self): ##revisar
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasa el usuario actual al formulario
        return kwargs

    def form_valid(self, form):
        """
        Crea una Nota
        """
        # Creo una nueva instancia de Nota y asigno sucursal
        note = form.save(commit=False)
        
        note.user_made = self.request.user
        note.branch = self.request.user.branch  # Asigna directamente la sucursal del usuario
        
        branches = list(form.cleaned_data['branch'])
        print(branches)
        for branch in branches:
            new_note = Note()
            new_note.subject = note.subject
            new_note.label = note.label
            new_note.description = note.description
            new_note.user_made = note.user_made
            new_note.branch = branch    # Asigna la instancia de Branch seleccionada
            new_note.save()
        

        note.save()
        
        # Comenté esta sección, me da error -> Error 111 connecting to 127.0.0.1:6379. 111.
        # Send a global message using the send_global_message function
        send_global_message(f"A new note has been created: {note.subject}")

        return super().form_valid(form)




################## LIST ######################

class NoteListView(CustomUserPassesTestMixin, ListView):
    model = Note
    template_name = 'notes/notes_page.html'
    context_object_name = 'notes'
    paginate_by = 6
    
    def get_queryset(self):
        # Filtra los productos que no han sido eliminados suavemente
        #Filtra las notas dirigidas a la branch del user
        user = self.request.user
        return Note.objects.filter(deleted_at=None, branch=user.branch)


########################### DELETE ####################################

class NoteDeleteView(CustomUserPassesTestMixin, FormView):
    model = Note
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())