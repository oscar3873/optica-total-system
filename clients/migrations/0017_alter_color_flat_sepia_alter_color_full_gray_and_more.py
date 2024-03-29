# Generated by Django 4.2.3 on 2023-11-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_alter_healthinsurance_options_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='flat_sepia',
            field=models.BooleanField(blank=True, null=True, verbose_name='Sepia Plano'),
        ),
        migrations.AlterField(
            model_name='color',
            name='full_gray',
            field=models.BooleanField(blank=True, null=True, verbose_name='Gris'),
        ),
        migrations.AlterField(
            model_name='color',
            name='gray_gradient',
            field=models.BooleanField(blank=True, null=True, verbose_name='Gris Grad.'),
        ),
        migrations.AlterField(
            model_name='color',
            name='white',
            field=models.BooleanField(blank=True, null=True, verbose_name='Blanco'),
        ),
        migrations.AlterField(
            model_name='cristal',
            name='bifocal_fv',
            field=models.BooleanField(blank=True, null=True, verbose_name='Bifocal FV'),
        ),
        migrations.AlterField(
            model_name='cristal',
            name='bifocal_k',
            field=models.BooleanField(blank=True, null=True, verbose_name='Bifocal K'),
        ),
        migrations.AlterField(
            model_name='cristal',
            name='bifocal_pi',
            field=models.BooleanField(blank=True, null=True, verbose_name='Bifocal PI'),
        ),
        migrations.AlterField(
            model_name='cristal',
            name='monofocal',
            field=models.BooleanField(blank=True, null=True, verbose_name='Monofocal'),
        ),
        migrations.AlterField(
            model_name='cristal',
            name='progressive',
            field=models.BooleanField(blank=True, null=True, verbose_name='Progresivo'),
        ),
        migrations.AlterField(
            model_name='material',
            name='m_r8',
            field=models.BooleanField(blank=True, null=True, verbose_name='M_R8'),
        ),
        migrations.AlterField(
            model_name='material',
            name='mineral',
            field=models.BooleanField(blank=True, null=True, verbose_name='Mineral'),
        ),
        migrations.AlterField(
            model_name='material',
            name='organic',
            field=models.BooleanField(blank=True, null=True, verbose_name='Organico'),
        ),
        migrations.AlterField(
            model_name='material',
            name='policarbonato',
            field=models.BooleanField(blank=True, null=True, verbose_name='Policarbonato'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='antireflex',
            field=models.BooleanField(blank=True, null=True, verbose_name='Antireflex'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='filtro_azul',
            field=models.BooleanField(blank=True, null=True, verbose_name='Filtro Azul'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='fotocromatico',
            field=models.BooleanField(blank=True, null=True, verbose_name='Fotocromático'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='neutrosolar',
            field=models.BooleanField(blank=True, null=True, verbose_name='Neutrosolar'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='polarizado',
            field=models.BooleanField(blank=True, null=True, verbose_name='Polarizado'),
        ),
        migrations.AlterField(
            model_name='tratamient',
            name='ultravex',
            field=models.BooleanField(blank=True, null=True, verbose_name='Ultravex'),
        ),
    ]
