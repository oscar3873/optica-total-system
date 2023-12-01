from django.db.models.signals import post_save

from .models import User
from .utils import generate_profile_img_and_assign


def set_imagen_user(instance, created, **kwargs):
    if not instance.imagen:
        generate_profile_img_and_assign(instance)
post_save.connect(set_imagen_user, sender=User)


def auto_set_user_branch(instance, created, **kwargs):
    from branches.models import Branch
    try:
        user = User.objects.first()
        if user.is_staff and not user.branch:
            user.branch = Branch.objects.first()
            user.save()
    except User.DoesNotExist:
        pass
post_save.connect(auto_set_user_branch, sender=User)
