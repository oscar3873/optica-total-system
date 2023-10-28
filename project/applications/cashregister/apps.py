from django.apps import AppConfig


class CashregisterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.cashregister"

    def ready(self):
        import applications.cashregister.signals