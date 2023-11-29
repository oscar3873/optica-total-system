# Generated by Django 4.2.3 on 2023-09-28 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0003_alter_branch_objetives_managers'),
        ('notes', '0003_alter_label_user_made_alter_note_user_made'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='branches.branch', verbose_name='Sucursal'),
        ),
    ]