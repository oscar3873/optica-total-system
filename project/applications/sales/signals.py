from django.db.models.signals import post_migrate

from .models import PaymentMethod, PaymentType

def auto_set_payment_type(sender, **kwargs):
    branch_count = PaymentType.objects.count()

    if branch_count == 0:
        for type in ['Efectivo', 'Tarjeta de Credito', 'Tarjeta de Debito', 'Transferencia']:
            PaymentType.objects.create(
                name = type,
            )

        for method in ['Efectivo', 'Transferencia']:
            payment_type = PaymentType.objects.get(name=method)
            PaymentMethod.objects.create(
                name=method,
                type_method=payment_type
                )
post_migrate.connect(auto_set_payment_type)