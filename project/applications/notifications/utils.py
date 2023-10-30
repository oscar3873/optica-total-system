def get_notifications_JSON(notifications):
        if notifications:
            notif_list = []
            for notification in notifications:
                notif_list.append(
                    {
                    'details': notification.details,
                    'user_made': str(notification.user_made.get_full_name()),
                    'reference_obj_verbose_name': str(notification.content_object.__class__._meta.verbose_name),
                    'created_at': str(notification.created_at)
                    }
                )
            return {'notifications': notif_list}
        return {'nothing': 'No hay notificaciones'}