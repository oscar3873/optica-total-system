# Generated by Django 4.2.3 on 2023-11-11 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afip', '0012_optionaltype_optional_alter_code_in_generics'),
        ('branches', '0007_alter_branch_objetives_objetive'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='pos_afip',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch', to='afip.pointofsales', verbose_name='Punto de venta Afip'),
        ),
    ]
