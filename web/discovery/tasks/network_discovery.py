import datetime

import celery

from scapy.all import get_if_addr, conf
from celery import group
from celery.exceptions import WorkerTerminate, WorkerShutdown
from billiard.exceptions import TimeLimitExceeded, WorkerLostError
from discovery.models import Discovery, Scanner
from discovery.nmapy import NetworkMapper


@celery.current_app.task(
    queue='DiscoveryQueue',
    name='DiscoverySubTask',
    bind=True,
    autoretry_for=(TimeLimitExceeded, WorkerLostError, WorkerTerminate, WorkerShutdown),
    default_retry_delay=5,
    retry_kwargs={'max_retries': 5}
)
def network_discovery_subtask(*args, **kwargs):
    pk = kwargs.pop('instance', 0)
    target = kwargs.pop('target', '')
    if not Discovery.objects.filter(pk=pk).exists():
        raise ValueError(f"Wrong parameter for network scanner primary key: {pk}")
    if target is None or target == '':
        raise ValueError(f"Wrong parameter for network scanner target: {target}")
    instance = Discovery.objects.get(pk=pk)
    nmap = NetworkMapper(
        pk=pk, model=Discovery,
        target=target,
        ports=instance.ports()['TCP'],
        all_ip_address=len(instance.available_ip_address)
    )
    nmap.start()


@celery.current_app.task(
    queue='DiscoveryQueue',
    name='DiscoveryTask',
    bind=True,
    autoretry_for=(TimeLimitExceeded, WorkerLostError, WorkerTerminate, WorkerShutdown),
    default_retry_delay=5,
    retry_kwargs={'max_retries': 5}
)
def network_discovery_task(self, *args, **kwargs):
    pk = kwargs.pop('instance', 0)
    scanner_ip = get_if_addr(conf.iface)
    if not Discovery.objects.filter(pk=pk).exists():
        raise ValueError(f"Wrong parameter for network discovery primary key: {pk}")
    instance = Discovery.objects.get(pk=pk)
    if scanner_ip not in instance.available_ip_address:
        Discovery.add_node(pk=instance.pk, _model=Discovery, node={}, name=scanner_ip)
    result = group(
        [(network_discovery_subtask.s(target=ip, instance=pk)) for ip in instance.available_ip_address]
    ).apply_async()

    result.get(disable_sync_subtasks=False, propagate=False)

    Discovery.objects.filter(pk=pk).update(progress=100, ended_at=datetime.datetime.now())


@celery.current_app.task(
    queue='ScannerQueue',
    name='ScannerSubTask',
    bind=True,
    autoretry_for=(TimeLimitExceeded, WorkerLostError, WorkerTerminate, WorkerShutdown),
    default_retry_delay=5,
    retry_kwargs={'max_retries': 5}
)
def network_scanner_subtask(*args, **kwargs):
    pk = kwargs.pop('instance', 0)
    target = kwargs.pop('target', '')
    if not Scanner.objects.filter(pk=pk).exists():
        raise ValueError(f"Wrong parameter for network scanner primary key: {pk}")
    if target is None or target == '':
        raise ValueError(f"Wrong parameter for network scanner target: {target}")
    instance = Scanner.objects.get(pk=pk)
    nmap = NetworkMapper(
        pk=pk, model=Scanner,
        target=target,
        ports=instance.ports()['TCP'],
        all_ip_address=len(instance.available_ip_address)
    )
    nmap.start()


@celery.current_app.task(
    queue='ScannerQueue',
    name='ScannerTask',
    bind=True,
    autoretry_for=(TimeLimitExceeded, WorkerLostError, WorkerTerminate, WorkerShutdown),
    default_retry_delay=5,
    retry_kwargs={'max_retries': 5}
)
def network_scanner_task(self, *args, **kwargs):
    pk = kwargs.pop('instance', 0)
    scanner_ip = get_if_addr(conf.iface)
    if not Scanner.objects.filter(pk=pk).exists():
        raise ValueError(f"Wrong parameter for network scanner primary key: {pk}")
    instance = Scanner.objects.get(pk=pk)
    if scanner_ip not in instance.available_ip_address:
        Scanner.add_node(pk=instance.pk, _model=Scanner, node={}, name=scanner_ip)
    result = group(
        [(network_scanner_subtask.s(target=ip, instance=pk)) for ip in instance.available_ip_address]
    ).apply_async()

    result.get(disable_sync_subtasks=False, propagate=False)

    Scanner.objects.filter(pk=pk).update(progress=100, ended_at=datetime.datetime.now())

