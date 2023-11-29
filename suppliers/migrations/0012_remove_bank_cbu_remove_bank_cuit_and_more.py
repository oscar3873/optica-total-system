# Generated by Django 4.2.3 on 2023-11-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suppliers', '0011_alter_supplier_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='cbu',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='cuit',
        ),
        migrations.RemoveField(
            model_name='supplier_bank',
            name='bank',
        ),
        migrations.CreateModel(
            name='Cbu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cbu', models.CharField(blank=True, max_length=20, null=True, verbose_name='ALIAS/CBU/CVU')),
                ('cuit', models.CharField(blank=True, max_length=20, null=True, verbose_name='CUIT Proveedor')),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cbu', to='suppliers.bank', verbose_name='Banco')),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Por')),
            ],
            options={
                'verbose_name': 'ALIAS / CBU / CVU',
            },
        ),
        migrations.AddField(
            model_name='supplier_bank',
            name='banks',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='suppliers.cbu', verbose_name='Banco asociado'),
        ),
    ]