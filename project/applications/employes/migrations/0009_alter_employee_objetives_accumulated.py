# Generated by Django 4.2.3 on 2023-11-23 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0008_alter_employee_objetives_objetive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_objetives',
            name='accumulated',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Acumulado'),
        ),
    ]
