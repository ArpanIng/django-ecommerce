# Generated by Django 4.2.1 on 2023-06-05 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stores", "0002_review"),
    ]

    operations = [
        migrations.CreateModel(
            name="Variation",
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
                    "variation_category",
                    models.CharField(
                        choices=[("color", "Color"), ("size", "Size")], max_length=10
                    ),
                ),
                ("variation_value", models.CharField(max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stores.product"
                    ),
                ),
            ],
        ),
    ]
