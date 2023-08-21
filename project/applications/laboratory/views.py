from django.views.generic.edit import FormView
from .forms import LaboratoryForm

class LaboratoryCreateView(FormView):
    template_name = 'laboratory/create_form.html'
    form_class = LaboratoryForm
    success_url = 'core_app:home'

    def form_valid(self, form):
        print(form.cleaned_data)
        return None
