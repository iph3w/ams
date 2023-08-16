import socket
import fcntl
import struct
import json
from django.test import TestCase
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule
from celery.contrib.testing.worker import start_worker

from discovery.models import Discovery, Scanner
from app.celery import app


def get_ip_address_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address_info = {}
    for idx in socket.if_nameindex():
        if idx[1] != 'lo':
            interface = idx[1]
            ip = socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface, 'utf-8')))[20:24]
            )
            netmask = socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s', bytes(interface, 'utf-8')))[20:24]
            )
            ip_address_info[ip] = netmask
    return ip_address_info


class NetworkDiscoveryScheduledTaskTestCase(TestCase):
    def test_scheduled_network_discovery_task(self):
        ip_address_info = get_ip_address_info()
        number_of_tasks = 0
        crontab, _ = CrontabSchedule.objects.get_or_create(
            minute="0", hour="*", day_of_week="*", day_of_month="10-15", month_of_year="*"
        )
        for ip, netmask in ip_address_info.items():
            Discovery.objects.create(
                ip_address=ip,
                netmask=netmask,
                start_automatically=False,
                crontab=crontab
            )
            number_of_tasks += 1

        self.assertEqual(number_of_tasks, PeriodicTasks.objects.all().count())


class NetworkScannerScheduledTaskTestCase(TestCase):
    def test_scheduled_network_scanner_task(self):
        ip_address_info = get_ip_address_info()
        number_of_tasks = 0
        crontab, _ = CrontabSchedule.objects.get_or_create(
            minute="0", hour="*", day_of_week="*", day_of_month="10-15", month_of_year="*"
        )
        for ip, netmask in ip_address_info.items():
            Scanner.objects.create(
                ip_address=ip,
                netmask=netmask,
                start_automatically=False,
                crontab=crontab
            )
            number_of_tasks += 1

        self.assertEqual(number_of_tasks, PeriodicTasks.objects.all().count())
