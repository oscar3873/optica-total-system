# Generated by Django 4.2.3 on 2023-08-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0002_alter_branch_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
