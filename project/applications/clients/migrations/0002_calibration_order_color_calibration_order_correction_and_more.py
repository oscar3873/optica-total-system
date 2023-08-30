# Generated by Django 4.2.3 on 2023-08-30 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employes', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibration_order',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.color'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='correction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.correction'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='employees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='employes.employee'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='interpupillary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.interpupillary'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.material'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='tratamient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.tratamient'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='type_cristal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.cristal'),
        ),
        migrations.AddField(
            model_name='calibration_order',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='color',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='correction',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cristal',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer_healthinsurance',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='customer_insurance', to='clients.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_healthinsurance',
            name='h_insurance',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='customer_insurance', to='clients.healthinsurance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_healthinsurance',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthinsurance',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interpupillary',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tratamient',
            name='user_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
