# Generated by Django 4.2.3 on 2023-09-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_imagen_alter_user_address_alter_user_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Imagen de perfil'),
        ),
    ]
