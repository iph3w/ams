""" Initialize Device Type
"""
from django.core.management.base import BaseCommand
from inventory.models import DeviceType
from inventory.domain import DEVICES_TYPES


class Command(BaseCommand):
    """Initialize Device Types Command
    """
    help = 'Initializes Device Types Data'

    def handle(self, *args, **options):
        for device_type in DEVICES_TYPES:
            if DeviceType.objects.filter(name=device_type).exists() is False:
                obj = DeviceType.objects.create(name=device_type)
                self.stdout.write(self.style.SUCCESS(f'"{obj}" successfully added to database.'))
            else:
                self.stdout.write(self.style.WARNING(f'"{device_type}" already exists in database!'))
