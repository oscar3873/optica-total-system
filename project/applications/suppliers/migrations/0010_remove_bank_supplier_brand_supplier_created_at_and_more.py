# Generated by Django 4.2.3 on 2023-11-09 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suppliers', '0009_supplier_address_alter_supplier_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='supplier',
        ),
        migrations.AddField(
            model_name='brand_supplier',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='brand_supplier',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brand_supplier',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='brand_supplier',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Por'),
        ),
        migrations.CreateModel(
            name='Supplier_Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='suppliers.bank', verbose_name='Banco')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banks', to='suppliers.supplier', verbose_name='Proveedor')),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Por')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
