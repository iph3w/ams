"""Device Model
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class DeviceType(models.Model):
    """DeviceType Model

    Attributes:
        name (str): device type name
    """
    name = models.CharField(
        max_length=128,
        default='', null=False, blank=False,
        verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Device Type")
        verbose_name_plural = _("Device Types")

    def __str__(self) -> str:
        return str(self.name)


class Device(models.Model):
    """Device Model

    Attributes:
        name (str): device name
        device_type (DeviceType)
        serial (str)
        manufacturer (str)
        product (str)
        user (str)
        is_healthy (bool)
        ipv4_address (str)
        description (str)
    """
    name = models.CharField(
        max_length=128,
        default='', null=False, blank=False,
        verbose_name=_("Name"))
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name="devices")
    serial = models.CharField(
        max_length=128, unique=True,
        default='', null=False, blank=False,
        verbose_name=_("Serial"))
    manufacturer = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Manufacturer"))
    product = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Product"))
    user = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("User"))
    is_healthy = models.BooleanField(
        default=False, null=False, blank=False,
        verbose_name=_("Is Healthy"))
    ipv4_address = models.GenericIPAddressField(
        null=True, blank=True,
        verbose_name=_("IP Address"))
    description = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self) -> str:
        return f"{self.name}"
