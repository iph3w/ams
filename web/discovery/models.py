import typing
import uuid
import datetime
import json
import dataclasses
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from ipaddress import IPv4Network
from .domain import NetworkNode

# MAX_PORT_RANGE = 65536
MAX_PORT_RANGE = 1024
MIN_PORT_RANGE = 1

NODES_INDEX = "NODES"
EDGES_INDEX = "EDGES"


class Discovery(models.Model):
    __nodes: typing.Dict = {}
    __edges: typing.List = []

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
    graph = models.JSONField(
        null=True, blank=True, editable=False,
        verbose_name=_("Graph")
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
    def max_port(self) -> int:
        return MAX_PORT_RANGE

    @property
    def min_port(self) -> int:
        return MIN_PORT_RANGE

    def set_graph(self, graph_data: dict):
        self.graph = graph_data
        self.save()

    def set_progress(self, val):
        self.progress = val
        self.save()

    def finish_discovery(self, graph: str):
        self.ended_at = datetime.datetime.now()
        self.save()

    def get_status(self) -> dict:
        return {
            "status": {"progress": self.progress},
            "graph": self.graph
        }

    def add_node(self, node: NetworkNode, name: str):
        res = False
        if node is not None:
            self.__nodes[name] = dataclasses.asdict(node)
            res = True
        else:
            if name not in self.__nodes.keys():
                self.__nodes[name] = None
                res = True
        if res is True:
            self.graph = json.dumps(self.to_dict())
            self.save()

    def add_edge(self, node1: str, node2: str):
        if (node1, node2) not in self.__edges:
            self.__edges.append((node1, node2))
            self.graph = json.dumps(self.to_dict())
            self.save()

    def remove_node(self, name: str):
        if name in self.__nodes.keys():
            del self.__nodes[name]
            self.graph = json.dumps(self.to_dict())
            self.save()

    def to_dict(self) -> typing.Dict:
        return {NODES_INDEX: self.__nodes, EDGES_INDEX: self.__edges}

    def __str__(self) -> str:
        return f"{self.ip_range} {self.progress:.2f}%"

    class Meta:
        ordering = ['-pk']
