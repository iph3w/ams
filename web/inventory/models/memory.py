from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class Memory(models.Model):
    """_summary_

    Args:
        capacity (int): Memory capacity in Bytes
        manufacturer (str): Memory manufacturer
        bus (int): Memory Bus
        system (System): foreign key to related System
    """
    capacity = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name=_("Memory Capacity"))
    manufacturer = models.CharField(
        max_length=128, default='', null=True, blank=True,
        verbose_name=_("Memory Manufacture"))
    bus = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name=_("Bus"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="memories")
    
    def __str__(self) -> str:
        """_summary_

        Returns:
            str: string
        """
        return f'{self.manufacturer} - {self.bus} [{(self.capacity // 1_000_000_000)} GB]'
