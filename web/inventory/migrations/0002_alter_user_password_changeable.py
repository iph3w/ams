# Generated by Django 4.2.1 on 2023-06-13 23:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password_changeable",
            field=models.BooleanField(
                blank=True, default=None, null=True, verbose_name="Password Changeable"
            ),
        ),
    ]
