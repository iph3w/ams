from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class Printer(models.Model):
    caption = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Caption"))
    is_network = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Network"))
    is_local = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Local"))
    port_name = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Port Name"))
    is_published = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Published"))
    is_shared = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Shared"))
    shared_name = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Shared Name"))
    driver_name = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Driver Name"))
    device_id = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Device Id"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="printers")
    
    def __str__(self) -> str:
        return f'{self.caption} [port:{self.port_name}] [Shared:{self.is_shared}({self.shared_name})]'


class PrinterDriver(models.Model):
    caption = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Caption"))
    version = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("Version"))
    supported_platform = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Supported Platform")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="printer_drivers")
    
    def __str__(self) -> str:
        return f'{self.caption} [version:{self.version}]- {self.supported_platform}'
