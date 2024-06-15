# Generated by Django 4.2.13 on 2024-06-15 13:15

import apps.receipts.helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Receipt",
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
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="Created time",
                        null=True,
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Updated time", null=True
                    ),
                ),
                (
                    "restaurant_name",
                    models.CharField(max_length=255, verbose_name="restaurant name"),
                ),
                ("dated", models.DateTimeField(verbose_name="date and time")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="price"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.receipts.helpers.receipt_image_upload_path,
                    ),
                ),
                ("street", models.CharField(max_length=100, verbose_name="street")),
                ("city", models.CharField(max_length=100, verbose_name="city")),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="state"
                    ),
                ),
                ("country", models.CharField(max_length=100, verbose_name="country")),
                (
                    "postal_code",
                    models.CharField(max_length=20, verbose_name="postal code"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receipts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "receipt",
                "verbose_name_plural": "receipts",
                "ordering": ["-id"],
            },
        ),
    ]
