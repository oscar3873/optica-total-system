from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.core.views import CustomUserPassesTestMixin

from .forms import NoteCreateForm
# Create your views here.
class NoteCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, FormView):
    form_class = NoteCreateForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        note = form.save(commit=False)        
        note.user = self.request.user
        note.save()
        return super().form_valid(form)