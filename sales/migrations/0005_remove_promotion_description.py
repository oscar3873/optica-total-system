# Generated by Django 4.2.3 on 2023-10-16 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_remove_promotion_branch_promotion_producta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='description',
        ),
    ]
