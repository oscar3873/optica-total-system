# Generated by Django 4.2.3 on 2023-10-20 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0004_remove_promotion_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]
