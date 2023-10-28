from django.db.models.signals import post_migrate

from project.settings.base import DATE_NOW
from .models import Branch


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