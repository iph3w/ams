from rest_framework import serializers
from inventory.models import System, Motherboard


class SystemSerializer(serializers.HyperlinkedModelSerializer):
    boot_time = serializers.DateField(format=None, input_formats=['%Y%m%d%H%M%S.%f'])

    class Meta:
        model = System
        fields = (
            'operating_system_name', 'operating_system_architecture',
            'node', 'release', 'version', 'machine', 'processor', 'boot_time'
        )
