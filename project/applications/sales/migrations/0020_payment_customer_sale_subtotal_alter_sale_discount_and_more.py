# Generated by Django 4.2.3 on 2023-10-28 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_delete_credittransaction'),
        ('sales', '0019_alter_paymentmethod_name_alter_paymenttype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='clients.customer'),
        ),
        migrations.AddField(
            model_name='sale',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Subtotal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sale',
            name='discount',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Descuento'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='missing_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Saldo'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total'),
        ),
    ]