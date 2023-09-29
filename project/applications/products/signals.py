from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Feature_type, Feature, Product

@receiver(pre_save, sender=Feature_type)
def save_lower_type(sender, instance, **kwargs):
    instance.name = instance.name.lower()

@receiver(pre_save, sender=Feature)
def save_lower_type(sender, instance, **kwargs):
    instance.name = instance.name.lower()

@receiver(pre_save, sender=Product)
def prices(sender, instance, **kwargs):
    instance.suggested_price = instance.cost_price * 1.4