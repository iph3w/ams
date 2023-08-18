from django.test import TestCase
from app import celery_app
from discovery.models import Discovery, Scanner
from .utility import Utility


class StartNetworkTaskTestCase(Utility, TestCase):
    def setUp(self) -> None:
        ip_address_info = self.get_ip_address_info()
        self.number_of_tasks = 0
        for ip, netmask in ip_address_info.items():
            Discovery.objects.create(ip_address=ip, netmask=netmask, start_automatically=True, crontab=None)
            Scanner.objects.create(ip_address=ip, netmask=netmask, start_automatically=True, crontab=None)
            self.number_of_tasks += 2

        celery_inspect = celery_app.control.inspect()
        self.active_tasks = 0
        for worker, tasks in celery_inspect.active().items():
            self.active_tasks += len(tasks)

    def tearDown(self) -> None:
        Discovery.objects.all().delete()
        Scanner.objects.all().delete()

    def test_network_task(self):
        self.assertEqual(
            self.number_of_tasks,
            self.active_tasks
        )

        self.assertEqual(
            self.number_of_tasks,
            Discovery.objects.filter(start_automatically=True).count() +
            Scanner.objects.filter(start_automatically=True).count()
        )
