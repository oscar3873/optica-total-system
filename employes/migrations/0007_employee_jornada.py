# Generated by Django 4.2.3 on 2023-10-31 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0006_employee_created_at_employee_deleted_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='jornada',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]