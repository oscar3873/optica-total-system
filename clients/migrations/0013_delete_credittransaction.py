# Generated by Django 4.2.3 on 2023-10-24 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_credittransaction_sale'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CreditTransaction',
        ),
    ]