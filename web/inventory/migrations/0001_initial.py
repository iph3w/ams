# Generated by Django 4.2.1 on 2023-06-03 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeviceType",
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
                    "name",
                    models.CharField(default="", max_length=128, verbose_name="Name"),
                ),
            ],
            options={
                "verbose_name": "Device Type",
                "verbose_name_plural": "Device Types",
            },
        ),
        migrations.CreateModel(
            name="Motherboard",
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
                    "manufacturer",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Motherboard Manufacture",
                    ),
                ),
                (
                    "product",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Motherboard Product",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Motherboard Version",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="System",
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
                    "operating_system_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Operating System",
                    ),
                ),
                (
                    "operating_system_architecture",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Architecture",
                    ),
                ),
                (
                    "node",
                    models.CharField(
                        default="", max_length=128, unique=True, verbose_name="Node"
                    ),
                ),
                (
                    "release",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Release",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Version",
                    ),
                ),
                (
                    "machine",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Machine",
                    ),
                ),
                (
                    "processor",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Processor",
                    ),
                ),
                (
                    "boot_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Boot Time"
                    ),
                ),
                (
                    "motherboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.motherboard",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                    "username",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Username",
                    ),
                ),
                (
                    "fullname",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Fullname",
                    ),
                ),
                (
                    "local_account",
                    models.BooleanField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Local Account",
                    ),
                ),
                (
                    "password_changeable",
                    models.BooleanField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Password Changaeble",
                    ),
                ),
                (
                    "password_requires",
                    models.BooleanField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Password Requires",
                    ),
                ),
                (
                    "password_expires",
                    models.BooleanField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Password Expires",
                    ),
                ),
                (
                    "started_datetime",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Started Datetime",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrinterDriver",
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
                    "caption",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Caption",
                    ),
                ),
                (
                    "version",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Version"
                    ),
                ),
                (
                    "supported_platform",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Supported Platform",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="printer_drivers",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Printer",
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
                    "caption",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Caption",
                    ),
                ),
                (
                    "is_network",
                    models.BooleanField(
                        blank=True, default=None, null=True, verbose_name="Network"
                    ),
                ),
                (
                    "is_local",
                    models.BooleanField(
                        blank=True, default=None, null=True, verbose_name="Local"
                    ),
                ),
                (
                    "port_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Port Name",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        blank=True, default=None, null=True, verbose_name="Published"
                    ),
                ),
                (
                    "is_shared",
                    models.BooleanField(
                        blank=True, default=None, null=True, verbose_name="Shared"
                    ),
                ),
                (
                    "shared_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Shared Name",
                    ),
                ),
                (
                    "driver_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Driver Name",
                    ),
                ),
                (
                    "device_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Device Id",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="printers",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NetworkInterface",
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
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "mac_address",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="MAC Address",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="network_interfaces",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Memory",
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
                    "capacity",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Memory Capacity"
                    ),
                ),
                (
                    "manufacturer",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Memory Manufacture",
                    ),
                ),
                (
                    "bus",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Bus"
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memories",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IPV4",
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
                    "ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP Address"
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "network_interface",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ipv4_addresses",
                        to="inventory.networkinterface",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InstalledSoftware",
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
                    "caption",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Caption",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "install_date",
                    models.DateField(
                        blank=True, default=None, null=True, verbose_name="Install Date"
                    ),
                ),
                (
                    "install_location",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Install Location",
                    ),
                ),
                (
                    "vendor",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Vendor",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Version",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="installed_softwares",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DiskPartition",
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
                    "device",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Device",
                    ),
                ),
                (
                    "mount_point",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Mount Point",
                    ),
                ),
                (
                    "file_system_type",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="File System Type",
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="disk_partitions",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DiskDrive",
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
                    "manufacture",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Disk Manufacture",
                    ),
                ),
                (
                    "capacity",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Disk Capacity"
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="disk_drives",
                        to="inventory.system",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Device",
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
                    "name",
                    models.CharField(default="", max_length=128, verbose_name="Name"),
                ),
                (
                    "serial",
                    models.CharField(
                        default="", max_length=128, unique=True, verbose_name="Serial"
                    ),
                ),
                (
                    "manufacturer",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Manufacturer",
                    ),
                ),
                (
                    "product",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Product",
                    ),
                ),
                (
                    "user",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="User",
                    ),
                ),
                (
                    "is_healthy",
                    models.BooleanField(default=False, verbose_name="Is Healthy"),
                ),
                (
                    "ipv4_address",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP Address"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "device_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="devices",
                        to="inventory.devicetype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Device",
                "verbose_name_plural": "Devices",
            },
        ),
    ]
