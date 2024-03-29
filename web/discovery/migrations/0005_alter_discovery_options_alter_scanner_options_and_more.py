# Generated by Django 4.2.1 on 2023-06-13 21:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("discovery", "0004_alter_scanner_tcp_ports_alter_scanner_udp_ports"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="discovery",
            options={"verbose_name": "Discovery", "verbose_name_plural": "Discoveries"},
        ),
        migrations.AlterModelOptions(
            name="scanner",
            options={"verbose_name": "Scanner", "verbose_name_plural": "Scanners"},
        ),
        migrations.AddField(
            model_name="discovery",
            name="start_automatically",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="Start Automatically"
            ),
        ),
        migrations.AddField(
            model_name="scanner",
            name="start_automatically",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="Start Automatically"
            ),
        ),
    ]
