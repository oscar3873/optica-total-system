import copy

from applications.users.models import User
from applications.core.models import Person

def set_user_to_employee(employee, form):
    """
    Se crea un objeto Person con el que luego se crea un User para asignarlo al empleado y guardarlo.
    """    
    data = data_pop(form)
    person = Person.objects.create_person_dict(**data)

    password = form.cleaned_data['password1'] if len(form.cleaned_data['password1']) > 0 else 'opticatotal'
    username = form.cleaned_data['username']

    user = User.objects.create_user(
        role = 'EM',
        username = username, 
        email = person.email, 
        password = password,
        name = person.name,
        lastname = person.last_name,
        )
    
    employee.person = person
    employee.user = user
    employee.save()


def data_pop(form):
    """
    Devuelve los datos de un formulario para crear un empleado.
    """
    data = copy.copy(form.cleaned_data) # copio los datos de cleaned_data para pasarlos al manager de Person
    data.pop('from_branch')
    data.pop('address')
    data.pop('password1')
    data.pop('password2')
    data.pop('username')
    return data

