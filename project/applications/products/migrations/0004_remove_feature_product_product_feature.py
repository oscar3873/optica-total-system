# Generated by Django 4.2.3 on 2023-08-25 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0003_brand_user_made_category_user_made_feature_user_made_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='product',
        ),
        migrations.CreateModel(
            name='Product_feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_feature', to='products.feature', verbose_name='Caracteristica')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_feature', to='products.product', verbose_name='Producto')),
                ('user_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Producto x Categoria',
                'verbose_name_plural': 'Producto x Categoria',
            },
        ),
    ]
