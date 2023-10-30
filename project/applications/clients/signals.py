from django.db.models.signals import post_migrate

from .models import Customer

def auto_set_payment_type(sender, **kwargs):
    customer_count = Customer.objects.count()

    if customer_count == 0:
        Customer.objects.create(
            first_name = 'Anonimo',
            last_name = 'Anonimo',
            dni = '00000000',
            email = 'cliente.anonimo@gmail.com',
        )

post_migrate.connect(auto_set_payment_type)