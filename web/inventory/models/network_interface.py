from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class NetworkInterface(models.Model):
    """_summary_

    Args:
        name (str): name of the network interface
        mac_address (str): network interface MAC Address
        is_active (bool): specifies that if this ip is still assigned tothis device or not
        system (System): forigen key to System

    Returns:
        _type_: _description_
    """
    name = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("Name"))
    mac_address = models.CharField(
        max_length=128,
        default='', null=True, blank=True,
        verbose_name=_("MAC Address"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="network_interfaces")

    def __str__(self) -> str:
        return f'{self.name}'


class IPV4(models.Model):
    """_summary_

    Args:
        ip (_type_): IP Address
        is_active (bool): specifies that if this ip is still assigned tothis device or not
        network_interface (NetworkInterface): forigen key to NetworkInterface
    """
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP Address"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    network_interface = models.ForeignKey(
        NetworkInterface, on_delete=models.CASCADE, related_name="ipv4_addresses")
