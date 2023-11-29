# Generated by Django 4.2.3 on 2023-09-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('ADMINISTRADOR', 'ADMINISTRADOR'), ('EMPLEADO', 'EMPLEADO')], default='EMPLEADO', max_length=15, null=True, verbose_name='rol'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario'),
        ),
    ]