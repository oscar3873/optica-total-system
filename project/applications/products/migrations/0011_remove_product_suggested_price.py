# Generated by Django 4.2.3 on 2023-10-11 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_barcode_alter_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='suggested_price',
        ),
    ]
