# Generated by Django 4.2.3 on 2023-12-02 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alter_product_cost_price_alter_product_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Codigo'),
        ),
    ]