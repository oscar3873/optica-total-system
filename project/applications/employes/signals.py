from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *
from applications.users.utils import generate_profile_img_and_assign

@receiver(post_save, sender=Employee)
def set_imagen_user(instance, created, **kwargs):
    if not instance.user.imagen:
        generate_profile_img_and_assign(instance.user)

@receiver(pre_save, sender=Employee_Objetives)
def objetive_completed(instance, created, **kwargs):
    if not created:
        if instance.accumulated >= instance.objetive.quantity:
            instance.is_completed = True
