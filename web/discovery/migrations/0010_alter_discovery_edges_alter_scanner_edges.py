# Generated by Django 4.2.1 on 2023-08-17 06:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("discovery", "0009_remove_discovery_graph_remove_scanner_graph_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discovery",
            name="edges",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.CharField(
                        blank=True, default="", editable=False, null=True
                    ),
                    default=[],
                    size=2,
                ),
                default=[],
                size=None,
                verbose_name="Edges",
            ),
        ),
        migrations.AlterField(
            model_name="scanner",
            name="edges",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.CharField(
                        blank=True, default="", editable=False, null=True
                    ),
                    default=[],
                    size=2,
                ),
                default=[],
                size=None,
                verbose_name="Edges",
            ),
        ),
    ]