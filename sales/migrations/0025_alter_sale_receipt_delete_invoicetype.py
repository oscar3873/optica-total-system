# Generated by Django 4.2.3 on 2023-11-23 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afip', '0012_optionaltype_optional_alter_code_in_generics'),
        ('sales', '0024_remove_receipt_client_remove_receipt_user_made_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='receipt',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='afip.receipt'),
        ),
        migrations.DeleteModel(
            name='InvoiceType',
        ),
    ]
