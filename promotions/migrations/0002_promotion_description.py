# Generated by Django 4.2.3 on 2023-10-16 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripcion'),
        ),
    ]
