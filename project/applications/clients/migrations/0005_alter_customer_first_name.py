# Generated by Django 4.2.3 on 2023-09-16 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_calibration_order_user_made_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='nombre'),
        ),
    ]