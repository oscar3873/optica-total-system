# Generated by Django 4.2.3 on 2023-11-11 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0016_alter_supplier_bank_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier_bank',
            name='bank',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='suppliers.cbu', verbose_name='Banco asociado'),
        ),
    ]
