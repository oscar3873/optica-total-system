# Generated by Django 4.2.3 on 2023-10-26 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_product_promotion'),
        ('suppliers', '0004_supplier_phone_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand_Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
            options={
                'verbose_name': 'Marca por Proveedor',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cbu', models.CharField(max_length=20, verbose_name='CBU')),
                ('bank_name', models.CharField(max_length=50, verbose_name='Nombre del Banco')),
                ('cuit', models.CharField(blank=True, max_length=20, null=True, verbose_name='CUIT')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to='suppliers.supplier')),
            ],
            options={
                'verbose_name': 'Banco',
                'verbose_name_plural': 'Bancos',
            },
        ),
    ]
