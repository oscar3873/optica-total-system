# Generated by Django 4.2.3 on 2023-10-26 03:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_delete_credittransaction'),
        ('sales', '0016_alter_invoice_client_alter_invoice_invoice_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='date_time_sale',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='clients.customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='missing_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Saldo'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='state',
            field=models.CharField(choices=[('COMPLETADO', 'COMPLETADO'), ('PENDIENTE', 'PENDIENTE'), ('DEVOLUCION', 'DEVOLUCION'), ('CANCELADO', 'CANCELADO')], default='PENDIENTE', max_length=10, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total'),
        ),
    ]
