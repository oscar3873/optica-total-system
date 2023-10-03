from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .utils import generate_profile_img_and_assign


@receiver(post_save, sender=User)
def set_imagen_user(instance, created, **kwargs):
    if not instance.imagen:
        generate_profile_img_and_assign(instance)
