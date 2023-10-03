from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Employee
from applications.users.utils import generate_profile_img_and_assign

@receiver(post_save, sender=Employee)
def set_imagen_user(instance, created, **kwargs):
    if not instance.user.imagen:
        generate_profile_img_and_assign(instance.user)
