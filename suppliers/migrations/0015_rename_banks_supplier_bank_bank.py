# Generated by Django 4.2.3 on 2023-11-10 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0014_alter_cbu_cbu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier_bank',
            old_name='banks',
            new_name='bank',
        ),
    ]
