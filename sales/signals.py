from django.db.models.signals import post_migrate, post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from core.consumers import send_notifications
from notifications.models import Notifications
from notifications.utils import get_notifications_JSON 
from .models import PaymentMethod, PaymentType, Sale

def auto_set_payment_type(sender, **kwargs):
    branch_count = PaymentType.objects.count()

    if branch_count == 0:
        for type in ['Efectivo', 'Tarjeta de Credito', 'Tarjeta de Debito', 'Transferencia', 'Cuenta Corriente']:
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
            type_method=PaymentType.objects.get(name='Cuenta Corriente')
            )

post_migrate.connect(auto_set_payment_type)


@receiver(post_save, sender=Sale)
def set_notification(sender, created, instance, **kwargs):
    if created:
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
            pass
post_save.connect(set_notification, sender=Sale)


@receiver(post_save, sender=Sale)
def delete_notification(sender, instance, **kwargs):
    if instance.deleted_at is not None:
        try:
            # Elimina la notificación asociada a la instancia de Sale específica
            content_type = ContentType.objects.get_for_model(Sale)
            Notifications.objects.get(
                content_type=content_type,
                object_id=instance.pk
            ).delete()
        except Notifications.DoesNotExist:
            pass  # Puede que no exista una notificación asociada a la Sale, no hay problema

        try:
            # Elimina todas las notificaciones no asociadas a ninguna instancia de Sale
            content_type_sale = ContentType.objects.get_for_model(Sale)
            all_notifications = Notifications.objects.filter(content_type=content_type_sale, deleted_at=None)
            for notification in all_notifications:
                try:
                    Sale.objects.get(pk=notification.object_id)
                except Sale.DoesNotExist:
                    # Si no hay una instancia de Sale asociada, elimina la notificación
                    notification.delete()
        except Exception as e:
            print(e)
post_save.connect(delete_notification, sender=Sale)