# Generated by Django 4.2.3 on 2023-10-11 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_options_alter_product_branch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.PositiveBigIntegerField(null=True, verbose_name='Codigo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Precio'),
        ),
    ]
