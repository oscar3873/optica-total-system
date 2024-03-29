from django.contrib.contenttypes.models import ContentType

from core.consumers import send_notifications
from notifications.models import Notifications
from sales.models import Sale


def get_notifications_JSON(notifications):
        if notifications:
            notif_list = []
            for notification in notifications:
                notif_list.append(
                    {
                    'details': notification.details,
                    'user_made': str(notification.user_made.get_full_name()),
                    'avatarSrc': notification.user_made.imagen.url,
                    'reference_obj_verbose_name': str(notification.content_object.__class__._meta.verbose_name),
                    'created_at': str(notification.created_at),
                    'url': notification.content_object.get_absolute_url()
                    }
                )
            return {'notifications': notif_list}
        return {'nothing': 'No hay notificaciones'}


def set_notification(sale):
    content_type = ContentType.objects.get_for_model(Sale)
    
    notification = Notifications.objects.create(
        content_type = content_type,
        object_id = sale.id,
        details = '',
        user_made = sale.user_made
    )
    send_notifications(get_notifications_JSON([notification]))