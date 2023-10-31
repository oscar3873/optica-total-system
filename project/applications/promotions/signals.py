from django.db.models.signals import post_migrate

from .models import TypePromotion

def auto_set_promotions(sender, **kwargs):
    promo_count = TypePromotion.objects.count()

    if promo_count == 0:
        for type in ['2x1', '2da unidad', 'Descuento']:
            TypePromotion.objects.create(
                name = type,
            )
post_migrate.connect(auto_set_promotions)