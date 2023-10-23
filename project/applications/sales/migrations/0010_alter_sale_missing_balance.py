# Generated by Django 4.2.3 on 2023-10-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_sale_missing_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='missing_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
