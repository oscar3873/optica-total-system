# Generated by Django 4.2.3 on 2023-08-30 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cashregister", "0003_remove_cashregister_is_active_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CashRegisterDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "registered_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "counted_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("difference", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "cash_register",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cashregister.cashregister",
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cashregister.paymentmethod",
                    ),
                ),
                (
                    "user_made",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
