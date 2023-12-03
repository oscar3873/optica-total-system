from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver

from .models import *

@receiver(pre_save, sender=Feature_type)
def save_lower_type(sender, instance, **kwargs):
    instance.name = instance.name.lower()

@receiver(pre_save, sender=Feature)
def save_lower_type(sender, instance, **kwargs):
    instance.name = instance.name.lower()

@receiver(pre_save, sender=Product)
def prices(sender, instance, **kwargs):
    instance.suggested_price = instance.cost_price * 1.4

def auto_set_category(sender, **kwargs):
    category_count = Category.objects.count()
    
    if category_count == 0:
        for category in ['Armazon', 'Cristal']:
            Category.objects.create(
                name=category,
            )
post_migrate.connect(auto_set_category)