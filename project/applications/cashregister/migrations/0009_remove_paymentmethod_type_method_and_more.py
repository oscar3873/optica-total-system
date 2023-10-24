# Generated by Django 4.2.3 on 2023-10-24 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_payment_sale_payment_paymenttype_paymentmethod_and_more'),
        ('cashregister', '0008_cashregister_observations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='type_method',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='user_made',
        ),
        migrations.RemoveField(
            model_name='paymenttype',
            name='user_made',
        ),
        migrations.AlterField(
            model_name='cashregisterdetail',
            name='type_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.paymenttype'),
        ),
        migrations.AlterField(
            model_name='movement',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.paymenttype', verbose_name='Metodo de pago'),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.DeleteModel(
            name='PaymentType',
        ),
    ]
