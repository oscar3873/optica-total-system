# Generated by Django 4.2.3 on 2023-10-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_has_eyeglass_frames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='has_eyeglass_frames',
            field=models.BooleanField(default=False, verbose_name='Armazón'),
        ),
    ]
