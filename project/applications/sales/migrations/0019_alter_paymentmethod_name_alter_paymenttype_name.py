# Generated by Django 4.2.3 on 2023-10-27 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_sale_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Metodo de Pago'),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Tipo de Pago'),
        ),
    ]
