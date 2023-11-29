from django.db.models.signals import post_migrate, pre_save

from project.settings import DATE_NOW
from .models import Branch, Branch_Objetives

def auto_set_branch(sender, **kwargs):
    branch_count = Branch.objects.count()

    if branch_count == 0:
        Branch.objects.create(
            name="Sucursal 1",
            address="Calle 111",
            open_hs=DATE_NOW.time(),
            close_hs=DATE_NOW.time(),
            phone='111111111'
        )
post_migrate.connect(auto_set_branch)


def objetive_completed(instance, **kwargs):
    if instance.accumulated >= instance.objetive.quantity:
        instance.is_completed = True
pre_save.connect(objetive_completed, sender=Branch_Objetives)