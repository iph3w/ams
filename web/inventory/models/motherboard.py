from django.db import models
from django.utils.translation import gettext_lazy as _


class Motherboard(models.Model):
    manufacturer = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Motherboard Manufacture")
    )
    product = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Motherboard Product")
    )
    version = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Motherboard Version")
    )

    def __str__(self) -> str:
        return f'{self.manufacturer} - {self.product} [{self.version}]'
