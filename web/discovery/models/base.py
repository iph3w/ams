import typing
import uuid
import datetime
from abc import abstractmethod
from ipaddress import IPv4Network
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule


NODES_INDEX = "NODES"
EDGES_INDEX = "EDGES"


class BaseDiscoveryModel(models.Model):
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
    start_automatically = models.BooleanField(
        default=False, verbose_name=_("Start Automatically")
    )
    created_by = models.ForeignKey(
        to=User, null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name=_("Created By")
    )

    crontab = models.ForeignKey(
        CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Crontab Schedule'),
        help_text=_('Crontab Schedule to run the task on.  '
                    'Set only one schedule type, leave the others null.'),
    )

    nodes = models.JSONField(
        null=True, blank=True, editable=False, default=dict,
        verbose_name=_("Nodes")
    )

    edges = ArrayField(
        ArrayField(
            models.CharField(null=True, blank=True, editable=False, default=''),
            size=2,
            default=list
        ), default=list,
        verbose_name=_("Edges")
    )

    @staticmethod
    @transaction.atomic()
    def set_progress(pk: int, _model, name: str):
        instance = _model.objects.get(pk=pk)
        if name in instance.nodes.keys():
            if 'progress' in instance.nodes[name].keys():
                instance.nodes[name]['progress'] = len(instance.ports()['TCP'])
                instance.save()

    def finish_discovery(self):
        self.ended_at = datetime.datetime.now()
        self.save()

    def get_status(self) -> dict:
        return {
            "status": {"progress": self.progress},
            "graph": self.graph
        }

    @property
    def graph(self) -> typing.Dict:
        return {NODES_INDEX: self.nodes, EDGES_INDEX: self.edges}

    @staticmethod
    @transaction.atomic
    def add_node(pk: int, _model, node: dict, name: str):
        instance = _model.objects.get(pk=pk)
        res = False
        if node is not None and len(node.keys()) > 0:
            instance.nodes[name] = node
            res = True
        else:
            if name not in instance.nodes.keys():
                instance.nodes[name] = {}
                res = True
        if res is True:
            progress = 0
            for _, n in instance.nodes.items():
                if 'progress' in n.keys():
                    print(_ + ' -> ' + str(n['progress']))
                    progress += (n['progress'] / 100) * len(instance.ports()['TCP'])
            print(progress)
            instance.progress = (progress / (len(instance.available_ip_address) * len(instance.ports()['TCP']))) * 100
            print(instance.progress)
            instance.save()

    @staticmethod
    @transaction.atomic
    def add_edge(pk: int, _model, node1: str, node2: str):
        instance = _model.objects.get(pk=pk)
        if [node1, node2] not in instance.edges:
            instance.edges.append([node1, node2])
            instance.save()

    @staticmethod
    @transaction.atomic
    def remove_node(pk: int, _model, name: str):
        instance = _model.objects.get(pk=pk)
        if name in instance.nodes.keys():
            instance.nodes.pop(name)
            instance.save()

    def __str__(self) -> str:
        return f"{self.ip_range} {self.progress:.2f}%"

    @property
    def available_ip_address(self):
        return [str(ip) for ip in IPv4Network(self.ip_range)]

    @property
    def ip_range(self) -> str:
        try:
            prefix = IPv4Network(f"{self.ip_address}/{self.netmask}").prefixlen
            return f"{self.ip_address}/{prefix}"
        except Exception as ex:
            print(ex)
            return "N/A"

    @abstractmethod
    def ports(self) -> typing.Dict:
        raise NotImplementedError

    class Meta:
        ordering = ['-pk']
        abstract = True
