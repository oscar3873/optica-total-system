# Generated by Django 4.2.3 on 2023-11-15 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_objetives_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetives',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='objetives',
            name='exp_date',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de finalizacion'),
        ),
        migrations.AlterField(
            model_name='objetives',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nicio'),
        ),
        migrations.AlterField(
            model_name='objetives',
            name='title',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='objetives',
            name='to',
            field=models.CharField(blank=True, choices=[('EMPLEADOS', 'EMPLEADOS'), ('SUCURSAL', 'SUCURSAL')], default='EMPLEADOS', max_length=9, null=True, verbose_name='Para'),
        ),
    ]
