from tokenize import blank_re
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .motherboard import Motherboard


class System(models.Model):
    operating_system_name = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Operating System")
    )
    operating_system_architecture = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Architecture")
    )
    node = models.CharField(
        max_length=128, default='', null=False, blank=False, verbose_name=_("Node"), unique=True
    )
    release = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Release")
    )
    version = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Version")
    )
    machine = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Machine")
    )
    processor = models.CharField(
        max_length=128, default='', null=True, blank=True, verbose_name=_("Processor")
    )
    boot_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Boot Time")
    )
    motherboard = models.OneToOneField(Motherboard, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.node} ({self.operating_system_name} {self.release}) - {self.boot_time}"

    def memory_capacity(self) -> int:
        result = self.memories.aggregate(Sum("capacity"))
        if result is not None and 'capacity__sum' in result.keys() and result['capacity__sum'] is not None:
            return int(result['capacity__sum'])
        return 0
    
    def disk_capacity(self) -> int:
        result = self.disk_drives.aggregate(Sum("capacity"))
        if result is not None and 'capacity__sum' in result.keys() and result['capacity__sum'] is not None:
            return int(result['capacity__sum'])
        return 0
