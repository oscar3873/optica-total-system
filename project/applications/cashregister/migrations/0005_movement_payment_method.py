# Generated by Django 4.2.3 on 2023-09-11 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashregister', '0004_rename_typemethodepayment_paymenttype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashregister.paymenttype', verbose_name='Metodo de pago'),
        ),
    ]
