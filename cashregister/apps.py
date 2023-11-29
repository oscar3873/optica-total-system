from django.apps import AppConfig


class CashregisterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cashregister"

    def ready(self):
        import cashregister.signals