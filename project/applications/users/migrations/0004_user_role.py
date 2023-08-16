# Generated by Django 4.2.3 on 2023-08-15 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_email_alter_user_lastname_alter_user_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('AD', 'Administrador'), ('EM', 'Empleado')], default='EM', max_length=2),
        ),
    ]