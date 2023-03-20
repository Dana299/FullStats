# Generated by Django 4.1.7 on 2023-03-14 23:00

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
            name="ProductTracking",
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
                ("product_id", models.PositiveIntegerField()),
                (
                    "tracking_interval",
                    models.IntegerField(
                        choices=[
                            (1, "One Hour"),
                            (12, "Twelve Hours"),
                            (24, "One Day"),
                        ],
                        default=12,
                    ),
                ),
                ("start_tracking_date", models.DateTimeField()),
                ("end_tracking_date", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductHistory",
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
                ("name", models.CharField(max_length=255)),
                ("price", models.PositiveIntegerField()),
                ("discount_price", models.PositiveIntegerField()),
                ("brand", models.CharField(max_length=120)),
                ("supplier", models.CharField(max_length=120)),
                ("last_updated", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stats.producttracking",
                    ),
                ),
            ],
        ),
    ]