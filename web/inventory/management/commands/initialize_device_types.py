""" Initialize Device Type
"""
from django.core.management.base import BaseCommand
from inventory.models import DeviceType


class Command(BaseCommand):
    """Initialize Device Types Commad
    """
    help = 'Initializes Device Types Data'

    def handle(self, *args, **options):
        device_types = [
            'Attendance', 'Headset', 'ATM', 'Pin Pad', 'Card Printer', 'Dot Matrix Printer',
            'Laser Printer', 'Speaker', 'WebCam', 'Scanner', 'Monitor', 'Network Switch', 'Router',
            'Network Camera', 'NVR', 'DVR'
        ]
        for device_type in device_types:
            if DeviceType.objects.filter(name=device_type).exists() is False:
                obj = DeviceType.objects.create(name=device_type)
                self.stdout.write(self.style.SUCCESS(f'"{obj}" successfully added to database.'))
            else:
                self.stdout.write(self.style.WARNING(f'"{device_type}" already exists in database!'))
