# Generated by Django 4.2.3 on 2023-08-26 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_rename_name_customer_first_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Material', 'verbose_name_plural': 'Materiales'},
        ),
    ]
