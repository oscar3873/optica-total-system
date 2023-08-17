import copy

from .models import Customer
from applications.core.models import Person

def set_person_to_customer(form):
    data = data_pop(form)

    Customer.objects.create_customer(
        person = Customer.objects.create_person_dict(**data),
        address = form.cleaned_data['address'],
    )


def data_pop(form):
    data = copy.copy(form.cleaned_data) # copio los datos de cleaned_data para pasarlos al manager de Person
    data.pop('address')
    return data