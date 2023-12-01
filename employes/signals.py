from django.db.models.signals import post_save, pre_save

from .models import *
from users.utils import generate_profile_img_and_assign

def set_imagen_user(instance, created, **kwargs):
    if not instance.user.imagen:
        generate_profile_img_and_assign(instance.user)
post_save.connect(set_imagen_user, sender=Employee)


def objetive_completed(instance, created, **kwargs):
    if instance.accumulated >= instance.objetive.quantity:
        instance.is_completed = True
post_save.connect(objetive_completed, sender=Employee_Objetives)