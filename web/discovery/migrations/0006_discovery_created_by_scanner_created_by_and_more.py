# Generated by Django 4.2.1 on 2023-06-15 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("discovery", "0005_alter_discovery_options_alter_scanner_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="discovery",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AddField(
            model_name="scanner",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="discovery",
            name="start_automatically",
            field=models.BooleanField(
                default=False, verbose_name="Start Automatically"
            ),
        ),
        migrations.AlterField(
            model_name="scanner",
            name="start_automatically",
            field=models.BooleanField(
                default=False, verbose_name="Start Automatically"
            ),
        ),
    ]
