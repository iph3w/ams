import typing
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from discovery.domain import popular_tcp_ports, popular_udp_ports
from .base import BaseDiscoveryModel


class Scanner(BaseDiscoveryModel):
    tcp_ports = ArrayField(
        base_field=models.IntegerField(default=0, blank=True),
        default=popular_tcp_ports,
        verbose_name=_("TCP Ports")
    )

    udp_ports = ArrayField(
        base_field=models.IntegerField(default=0, blank=True),
        default=popular_udp_ports,
        verbose_name=_("UDP Ports")
    )

    def ports(self) -> typing.Dict:
        return {
            'TCP': self.tcp_ports,
            'UDP': self.udp_ports
        }

    def __str__(self):
        return f"{self.__class__.__name__} - {super(Scanner, self).__str__()}"

    class Meta:
        verbose_name = _("Scanner")
        verbose_name_plural = _("Scanners")
