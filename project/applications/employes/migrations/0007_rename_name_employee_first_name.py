# Generated by Django 4.2.3 on 2023-08-25 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0006_alter_employee_user_made'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='name',
            new_name='first_name',
        ),
    ]
