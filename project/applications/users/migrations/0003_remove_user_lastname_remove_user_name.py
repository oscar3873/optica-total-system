# Generated by Django 4.2.3 on 2023-08-17 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email_alter_user_lastname_alter_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
