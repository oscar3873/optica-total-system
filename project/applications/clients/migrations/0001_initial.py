<<<<<<< HEAD
# Generated by Django 4.2.3 on 2023-09-07 13:57
=======
# Generated by Django 4.2.3 on 2023-09-07 00:22
>>>>>>> 8057cdb8de2af27191a3b8ab54121bd2551f8411

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(db_index=True, max_length=50)),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('dni', models.CharField(db_index=True, max_length=20, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Tratamient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('antireflex', models.BooleanField(blank=True, null=True)),
                ('filtro_azul', models.BooleanField(blank=True, null=True)),
                ('fotocromatico', models.BooleanField(blank=True, null=True)),
                ('ultravex', models.BooleanField(blank=True, null=True)),
                ('polarizado', models.BooleanField(blank=True, null=True)),
                ('neutrosolar', models.BooleanField(blank=True, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('policarbonato', models.BooleanField(blank=True, null=True)),
                ('organic', models.BooleanField(blank=True, null=True)),
                ('mineral', models.BooleanField(blank=True, null=True)),
                ('m_r8', models.BooleanField(blank=True, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interpupillary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('lej_od_nanopupilar', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_od_pelicula', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_oi_nanopupilar', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_oi_pelicula', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_total', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_od_nanopupilar', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_od_pelicula', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_oi_nanopupilar', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_oi_pelicula', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_total', models.CharField(blank=True, max_length=10, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HealthInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('cuit', models.CharField(max_length=20)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Obra Socail',
                'verbose_name_plural': 'Obras Socailes',
            },
        ),
        migrations.CreateModel(
            name='Customer_HealthInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_insurance', to='clients.customer')),
                ('h_insurance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_insurance', to='clients.healthinsurance')),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cristal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('monofocal', models.BooleanField(blank=True, null=True)),
                ('bifocal_fv', models.BooleanField(blank=True, null=True)),
                ('bifocal_k', models.BooleanField(blank=True, null=True)),
                ('bifocal_pi', models.BooleanField(blank=True, null=True)),
                ('progressive', models.BooleanField(blank=True, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('lej_od_esferico', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_od_cilindrico', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_od_eje', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_oi_esferico', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_oi_cilindrico', models.CharField(blank=True, max_length=10, null=True)),
                ('lej_oi_eje', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_od_esferico', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_od_cilindrico', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_od_eje', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_oi_esferico', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_oi_cilindrico', models.CharField(blank=True, max_length=10, null=True)),
                ('cer_oi_eje', models.CharField(blank=True, max_length=10, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('white', models.BooleanField(blank=True, null=True)),
                ('full_gray', models.BooleanField(blank=True, null=True)),
                ('gray_gradient', models.BooleanField(blank=True, null=True)),
                ('flat_sepia', models.BooleanField(blank=True, null=True)),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Calibration_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_done', models.BooleanField(blank=True, default=False, null=True)),
                ('diagnostic', models.CharField(blank=True, max_length=200, null=True)),
                ('armazon', models.CharField(blank=True, max_length=100, null=True)),
                ('observations', models.CharField(blank=True, max_length=200, null=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.color')),
                ('correction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.correction')),
                ('interpupillary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.interpupillary')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.material')),
                ('tratamient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.tratamient')),
                ('type_cristal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='laboratory', to='clients.cristal')),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
