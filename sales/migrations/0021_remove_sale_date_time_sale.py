# Generated by Django 4.2.3 on 2023-10-31 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0020_payment_customer_sale_subtotal_alter_sale_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='date_time_sale',
        ),
    ]
