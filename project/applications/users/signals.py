from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .utils import generate_profile_img_and_assign


def set_imagen_user(instance, **kwargs):
    if not instance.imagen:
        generate_profile_img_and_assign(instance)
post_save.connect(set_imagen_user, sender=User)
