from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.clients"

    def ready(self):
        import applications.clients.signals