import ast
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .motherboard import Motherboard


class Node(models.Model):
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP Address"), unique=True)
    str_ports = models.CharField(max_length=2048, default='', null=True, blank=True, verbose_name=_("Ports"))
    str_traceroute = models.CharField(
        max_length=2048, default='', null=True, blank=True, verbose_name=_("Traceroute"), unique=True
    )
    str_graph = models.CharField(max_length=4096, default='', null=True, blank=True, verbose_name=_("Graph"))
    
    def __str__(self) -> str:
        return f"{self.ip} ({self.ports}) - {self.boot_time}"

    def ports(self) -> list:
        return [x.strip() for x in ast.literal_eval(self.str_ports)]
    
    def traceroute(self) -> list:
        return [x.strip() for x in ast.literal_eval(self.str_traceroute)]
