from django.db.models.signals import post_migrate

from .models import Customer

def auto_set_payment_type(sender, **kwargs):
    customer_count = Customer.objects.count()

    if customer_count == 0:
        Customer.objects.create(
            first_name = 'Final',
            last_name = 'Consumidor',
            dni = '0',
        )
post_migrate.connect(auto_set_payment_type)