# Generated by Django 4.2.3 on 2023-12-14 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0009_alter_employee_objetives_accumulated'),
        ('sales', '0027_sale_commision_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='commision_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='employes.employee'),
        ),
    ]
