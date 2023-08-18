from django.db.models import Max
from django.test import TestCase
from app import celery_app
from discovery.models import Discovery, Scanner
from .utility import Utility
from discovery.tasks import (
    network_discovery_task, network_discovery_subtask, network_scanner_subtask, network_scanner_task
)


class NetworkTaskTestCase(Utility, TestCase):
    def setUp(self) -> None:
        ip_address_info = self.get_ip_address_info()
        self.number_of_tasks = 0
        self.discoveries = []
        self.scanners = []
        for ip, netmask in ip_address_info.items():
            self.discoveries.append(
                Discovery.objects.create(ip_address=ip, netmask=netmask, start_automatically=False, crontab=None)
            )
            self.scanners.append(
                Scanner.objects.create(ip_address=ip, netmask=netmask, start_automatically=False, crontab=None)
            )
            self.number_of_tasks += 2

        celery_inspect = celery_app.control.inspect()
        self.active_tasks = 0
        for worker, tasks in celery_inspect.active().items():
            self.active_tasks += len(tasks)

    def tearDown(self) -> None:
        Discovery.objects.all().delete()
        Scanner.objects.all().delete()

    def test_network_task_raises_value_error(self):
        self.assertTrue(Discovery.objects.all())

        with self.assertRaises(ValueError):
            network_discovery_subtask.delay(
                target='192.168.1.1',
                instance=Discovery.objects.aggregate(Max('pk'))['pk__max'] + 1
            ).get()

        with self.assertRaises(ValueError):
            network_discovery_subtask.delay(
                target='',
                instance=Discovery.objects.aggregate(Max('pk'))['pk__max']
            ).get()

        self.assertTrue(Scanner.objects.all())

        with self.assertRaises(ValueError):
            network_scanner_subtask.delay(
                target='',
                instance=Scanner.objects.aggregate(Max('pk'))['pk__max']
            ).get()

        with self.assertRaises(ValueError):
            network_scanner_subtask.delay(
                target='192.168.1.1',
                instance=Scanner.objects.aggregate(Max('pk'))['pk__max'] + 1
            ).get()
