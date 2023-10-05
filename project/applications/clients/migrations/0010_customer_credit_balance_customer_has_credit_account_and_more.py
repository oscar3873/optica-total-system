# Generated by Django 4.2.3 on 2023-10-05 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_alter_customer_address_alter_customer_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='credit_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Saldo de Cuenta'),
        ),
        migrations.AddField(
            model_name='customer',
            name='has_credit_account',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Cuenta corriente'),
        ),
        migrations.CreateModel(
            name='CreditTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_transactions', to='clients.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Transacción de Cuenta Corriente',
                'verbose_name_plural': 'Transacciones de Cuenta Corriente',
            },
        ),
    ]
