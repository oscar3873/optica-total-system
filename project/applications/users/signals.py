from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .utils import generate_profile_img_and_assign

@receiver(post_save, sender=User)
def set_imagen_user(sender, instance, created, **kwargs):
    print('\n\n\n\n\n POST_SAVE \n\n\n\n')
    if created:
        generate_profile_img_and_assign(instance)
