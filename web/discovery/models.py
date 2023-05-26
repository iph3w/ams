import uuid
import json
import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from ipaddress import IPv4Network

# MAX_PORT_RANGE = 65536
MAX_PORT_RANGE = 1024
MIN_PORT_RANGE = 1


class Discovery(models.Model):
    ip_address = models.GenericIPAddressField(
        blank=False, null=False,
        default='0.0.0.0', verbose_name=_("IP Address")
    )
    netmask = models.GenericIPAddressField(
        blank=False, null=False,
        default='255.255.255.255', verbose_name=_("Netmask")
    )
    uuid = models.UUIDField(
        blank=False, null=False, unique=True, editable=False,
        verbose_name=_("UUID"), default=uuid.uuid4
    )
    progress = models.FloatField(
        blank=False, null=False, editable=False,
        default=0, verbose_name=_("Progress")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False, blank=False, null=False,
        verbose_name=_("Created at")
    )
    ended_at = models.DateTimeField(
        default=None,
        blank=True, null=True, editable=False,
        verbose_name="Ended at"
    )
    created_by = models.ForeignKey(
        get_user_model(),
        null=True, blank=True, editable=False,
        on_delete=models.SET_NULL,
        related_name="discovery_created_by",
        verbose_name=_("Created by")
    )
    graph = models.TextField(
        null=True, blank=True, editable=False,
        verbose_name=_("Graph"),
    )

    @property
    def available_ip_address(self):
        return [str(ip) for ip in IPv4Network(self.ip_range)]

    @property
    def ip_range(self) -> str:
        try:
            prefixlen = IPv4Network(f"{self.ip_address}/{self.netmask}").prefixlen
            return f"{self.ip_address}/{prefixlen}"
        except:
            return "N/A"

    @property
    def graph_as_dict(self) -> dict:
        try:
            return json.loads(self.graph)
        except:
            return {}

    @property
    def max_port(self) -> int:
        return MAX_PORT_RANGE

    @property
    def min_port(self) -> int:
        return MIN_PORT_RANGE

    def set_graph(self, graph_data: set):
        self.graph = graph_data
        self.save()

    def set_progress(self, val):
        self.progress = val
        self.save()

    def finish_discovery(self, graph: str):
        self.ended_at = datetime.datetime.now()
        self.graph = graph
        self.save()

    def __str__(self) -> str:
        return f"{self.ip_range} {self.progress:.2f}%"

    class Meta:
        ordering = ['-pk']


@receiver(post_save, sender=Discovery, dispatch_uid="run_discovery_task")
def run_discovery_task(sender, instance: Discovery, created, **kwargs):
    if created:
        # TODO: Run Celery Task
        pass
