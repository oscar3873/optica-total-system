# Generated by Django 4.2.3 on 2023-10-17 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0002_promotion_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Descripcion'),
        ),
    ]