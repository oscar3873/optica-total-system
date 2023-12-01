from django.db.models.signals import post_migrate, pre_save

from django.utils import timezone
from .models import Branch, Branch_Objetives

def auto_set_branch(sender, **kwargs):
    branch_count = Branch.objects.count()

    now = timezone.now()
    
    if branch_count == 0:
        Branch.objects.create(
            name="Sucursal 1",
            address="Calle 111",
            open_hs=now.time(),
            close_hs=now.time(),
            phone='111111111'
        )
post_migrate.connect(auto_set_branch)


def objetive_completed(instance, **kwargs):
    if instance.accumulated >= instance.objetive.quantity:
        instance.is_completed = True
pre_save.connect(objetive_completed, sender=Branch_Objetives)