# Generated by Django 4.2.3 on 2023-10-30 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0020_payment_customer_sale_subtotal_alter_sale_discount_and_more'),
        ('clients', '0013_delete_credittransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='sale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='service_order', to='sales.sale'),
        ),
    ]
