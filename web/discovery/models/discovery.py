import typing
from django.utils.translation import gettext_lazy as _
from discovery.domain import popular_tcp_ports, popular_udp_ports
from .base import BaseDiscoveryModel


class Discovery(BaseDiscoveryModel):
    def ports(self) -> typing.Dict:
        return {
            'TCP': popular_tcp_ports(),
            'UDP': popular_udp_ports()
        }

    def __str__(self):
        return f"{self.__class__.__name__} - {super(Discovery, self).__str__()}"

    class Meta:
        verbose_name = _("Discovery")
        verbose_name_plural = _("Discoveries")
