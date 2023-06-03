"""Hard Disk Model
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class DiskPartition(models.Model):
    """Disk Partition Model

    Attributes:
        device (str): disk partition
        mount_point (str): disk partition mount point
        file_system_type (str): disk partition file system type
        system (System): foreign key to System
    """
    device = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Device"))
    mount_point = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Mount Point"))
    file_system_type = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("File System Type"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="disk_partitions")
    
    def __str__(self) -> str:
        return f'{self.device}[{self.mount_point}] - {self.file_system_type}'


class DiskDrive(models.Model):
    """Disk Drive Model

    Attributes:
        manufacture (str): disk drive manufacture
        capacity (int): disk drive capacity in Bytes
        system (System): foreign key to System
    """
    manufacture = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Disk Manufacture"))
    capacity = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name=_("Disk Capacity"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="disk_drives")

    def __str__(self) -> str:
        return f'{self.manufacture} [{(self.capacity // 1_000_000_000)} GB]'
