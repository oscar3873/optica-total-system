# Generated by Django 4.2.3 on 2023-08-17 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0003_alter_employee_options_remove_employee_person_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Empleado', 'verbose_name_plural': 'Empleados'},
        ),
    ]
