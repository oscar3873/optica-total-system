# Generated by Django 4.2.3 on 2023-10-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_invoicetype_payment_sale_delete_sale_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicetype',
            name='id',
            field=models.PositiveIntegerField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
    ]