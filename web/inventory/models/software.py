from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class InstalledSoftware(models.Model):
    caption = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Caption")
    )
    description = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Description")
    )
    install_date = models.DateField(
        default=None, null=True, blank=True, verbose_name=_("Install Date")
    )
    install_location = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Install Location")
    )
    vendor = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Vendor")
    )
    version = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Version")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active")
    )
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, related_name="installed_softwares"
    )
    
    def __str__(self) -> str:
        return f'{self.caption} [{self.version}] - {self.vendor} - {self.install_date}'
