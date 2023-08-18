import copy

from applications.users.models import User
from applications.core.models import Person

def data_pop(form):
    """
    Devuelve los datos de un formulario para crear un empleado.
    """
    data = copy.copy(form.cleaned_data) # copio los datos de cleaned_data para pasarlos al manager de Person
    data.pop('password1')
    data.pop('password2')
    data.pop('email')
    data.pop('username')
    return data

