from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django_celery_beat.models import PeriodicTask, PeriodicTasks


class DefaultNetworkDiscoveryScannerTaskCommandTestCase(TestCase):
    def call_command(self):
        call_command("default_network_discovery_scanner_task")

    def test_add_default_network_discovery_scanner_task(self):
        self.call_command()
        self.assertEqual(1, PeriodicTasks.objects.all().count())
