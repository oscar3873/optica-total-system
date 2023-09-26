from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView, DeleteView
from django.db import transaction
from django.contrib import messages

from applications.core.mixins import CustomUserPassesTestMixin
from applications.core.consumers import send_global_message
from applications.branches.models import Branch
from .models import Note, Label
from .forms import NoteCreateForm, LabelCreateForm
from .utils import get_notes_JSON

class NoteCreateView(CustomUserPassesTestMixin, FormView):
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_app:note_list')

    def get_form_kwargs(self): ##revisar
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasa el usuario actual al formulario
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label_form'] = LabelCreateForm

        return context

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            # Creo una nueva instancia de Nota y asigno sucursal
            note = form.save(commit=False)
            
            note.user_made = self.request.user
            note.branch = self.request.user.branch  # Asigna directamente la sucursal del usuario
            
            branches = list(form.cleaned_data['branch'])
            for branch in branches:
                new_note = Note()
                new_note.subject = note.subject
                new_note.label = note.label
                new_note.description = note.description
                new_note.user_made = note.user_made
                new_note.branch = branch    # Asigna la instancia de Branch seleccionada
                new_note.save()
            

            note.save()
            send_global_message(get_notes_JSON(note))

            return HttpResponseRedirect(self.get_success_url())
        
    def form_invalid(self,form):
        messages.error(self.request,'ERROR')
        return super().form_invalid(form)
    

class NoteUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_app:note_list')

    def get_form_kwargs(self): ##revisar
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasa el usuario actual al formulario
        return kwargs

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)


class LabelCreateView(CustomUserPassesTestMixin, FormView):
    '''
    Crear una nueva label
    '''
    form_class = LabelCreateForm

    def form_valid(self,form):
        label = form.save(commit=False)
        label.user_made = self.request.user
        label.save()
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
            new_label_data = {
                'id' : label.id,
                'label' : label.label,
                'color' : label.color
            }
                # Si es una solicitud AJAX, devuelve una respuesta JSON
            return JsonResponse({'status': 'success', 'new_type': new_label_data})

################## LIST ######################

class NoteListView(CustomUserPassesTestMixin, ListView):
    model = Note
    template_name = 'notes/notes_page.html'
    context_object_name = 'notes'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()

        return context
    
    def get_queryset(self):
        branch = self.request.user.branch
        branch_actualy = self.request.session.get('branch_actualy')

        if  self.request.user.is_staff and branch_actualy:
            branch_actualy = Branch.objects.get(id=branch_actualy)
            # Si el usuario es administrador y hay una sucursal seleccionada en la sesión,
            return Note.objects.filter(branch=branch_actualy, deleted_at=None)
        
        # En otros casos, filtra por la sucursal del usuario
        return Note.objects.filter(branch=branch, deleted_at=None)


########################### DELETE ####################################

class NoteDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'
    success_url = reverse_lazy('core_app:home')
    
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())