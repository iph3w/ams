from datetime import datetime
from django.test import TestCase
from django_celery_beat.models import PeriodicTasks, CrontabSchedule

from discovery.models import Discovery, Scanner
from .utility import Utility


class NetworkScheduledTaskTestCase(Utility, TestCase):
    def setUp(self) -> None:
        self.crontab, _ = CrontabSchedule.objects.get_or_create(
            minute="*", hour=f"{datetime.now().hour + 1}", day_of_week="*", day_of_month="*", month_of_year="*"
        )
        self.ip_address_info = self.get_ip_address_info()

    def tearDown(self) -> None:
        Discovery.objects.all().delete()
        Scanner.objects.all().delete()
        PeriodicTasks.objects.all().delete()

    def test_scheduled_network_discovery_task(self):
        number_of_tasks = 0
        for ip, netmask in self.ip_address_info.items():
            Discovery.objects.create(
                ip_address=ip, netmask=netmask, start_automatically=False,
                crontab=self.crontab
            )
            number_of_tasks += 1

        self.assertEqual(number_of_tasks, PeriodicTasks.objects.all().count())

    def test_scheduled_network_scanner_task(self):
        number_of_tasks = 0
        for ip, netmask in self.ip_address_info.items():
            Scanner.objects.create(
                ip_address=ip, netmask=netmask, start_automatically=False,
                crontab=self.crontab
            )
            number_of_tasks += 1

        self.assertEqual(number_of_tasks, PeriodicTasks.objects.all().count())
