import random

from django.test import TestCase
from django.core.management import call_command
from inventory.models import DeviceType
from inventory.domain import DEVICES_TYPES


class InitializeDeviceTypeCommandTestCase(TestCase):
    def call_command(self):
        call_command("initialize_device_types")

    def make_sure_all_devices_are_added_to_database(self) -> bool:
        for device_type in DEVICES_TYPES:
            if DeviceType.objects.filter(name=device_type).exists() is False:
                return False
        return True

    def test_run_command_for_first_time(self):
        self.call_command()
        self.assertEqual(len(DEVICES_TYPES), DeviceType.objects.all().count())
        self.assertTrue(self.make_sure_all_devices_are_added_to_database())

    def test_try_to_run_command_again(self):
        self.call_command()
        self.call_command()
        self.assertEqual(len(DEVICES_TYPES), DeviceType.objects.all().count())
        self.assertTrue(self.make_sure_all_devices_are_added_to_database())

    def test_try_to_run_command_for_first_time_but_one_of_device_types_is_already_added_to_database(self):
        DeviceType.objects.create(
            name=DEVICES_TYPES[random.randint(0, len(DEVICES_TYPES) - 1)]
        )
        self.call_command()
        self.assertEqual(len(DEVICES_TYPES), DeviceType.objects.all().count())
        self.assertTrue(self.make_sure_all_devices_are_added_to_database())

    def test_try_to_run_command_for_first_time_but_another_device_types_is_already_added_to_database(self):
        DeviceType.objects.create(
            name="SAMPLE_DEVICE_TYPE"
        )
        self.call_command()
        self.assertEqual(len(DEVICES_TYPES) + 1, DeviceType.objects.all().count())
        self.assertTrue(self.make_sure_all_devices_are_added_to_database())
