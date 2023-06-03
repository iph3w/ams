"""Device Admin
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from inventory.models import DeviceType


class DeviceTypeAdmin(admin.ModelAdmin):
    """DeviceType Admin Model
    """
    list_display = [
        "name",
        "show_devices",
        ]

    search_fields = [
        "name",
    ]

    def show_devices(self, obj: DeviceType) -> str:
        """show devices categorized by this device type

        Args:
            obj (DeviceType): _description_

        Returns:
            str: number of devices related to this device type
        """
        return f"{obj.devices.count()}"
    show_devices.short_description = _("NO of Devices")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('devices')


class DeviceAdmin(admin.ModelAdmin):
    """Device Admin Model
    """
    list_select_related = ('device_type',)

    list_display = [
        "name",
        "device_type",
        "serial",
        "manufacturer",
        "product",
        "user",
        "is_healthy",
        "ipv4_address"
        ]

    search_fields = [
        "name",
        "serial",
        "manufacturer",
        "product",
        "user",
        "ipv4_address"
    ]

    list_filter = [
        "device_type__name",
        "manufacturer",
        "is_healthy",
        ]

    autocomplete_fields = ["device_type"]
