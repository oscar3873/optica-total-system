# Generated by Django 4.2.3 on 2023-11-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashregister', '0009_remove_paymentmethod_type_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripción'),
        ),
    ]
