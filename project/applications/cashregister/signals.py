from django.db.models.signals import post_migrate

from .models import Currency

def auto_set_currency(sender, **kwargs):
    currencies = Currency.objects.count()

    if currencies == 0:
        Currency.objects.create(
            name = 'PESO',
            symbol = '$',
            code = 'ARS'
        )
post_migrate.connect(auto_set_currency)