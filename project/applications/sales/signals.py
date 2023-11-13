from django.db.models.signals import post_migrate, post_save
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from applications.core.consumers import send_notifications
from applications.notifications.models import Notifications
from applications.notifications.utils import get_notifications_JSON 
from .models import PaymentMethod, PaymentType, Sale

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
        PaymentMethod.objects.create(
            name='Cuenta Corriente',
            type_method=PaymentType.objects.get(name='Tarjeta de Credito')
            )

post_migrate.connect(auto_set_payment_type)


@receiver(post_save, sender=Sale)
def set_notification(sender, instance, **kwargs):
    try:
        content_type = ContentType.objects.get_for_model(Sale)

        notification = Notifications.objects.create(
            content_type=content_type,
            object_id=instance.id,
            details='',
            user_made=instance.user_made
        )
        
        # Try to send the notification via Redis
        send_notifications(get_notifications_JSON([notification]))

    except Exception as e:
        # Handle the exception (e.g., print a warning, log it, or perform alternative actions)
        print(f"An error occurred while sending notification: {e}")

# Connect the signal
post_save.connect(set_notification, sender=Sale)