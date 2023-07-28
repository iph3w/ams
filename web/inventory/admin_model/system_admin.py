from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from inventory.models import System


class SystemAdmin(admin.ModelAdmin):
    readonly_fields = [
        "operating_system_name",
        "operating_system_architecture",
        "node",
        "release",
        "version",
        "machine",
        "processor",
        "boot_time",
        "motherboard",
    ]
    
    list_display = [
        "node",
        "operating_system_name",
        "version",
        "processor",
        "motherboard__manufacturer",
        "motherboard__product",
        "show_memory_capacity",
        "show_disk_capacity"
    ]

    search_fields = [
        "operating_system_name",
        "operating_system_architecture",
        "release",
        "machine",
        "processor",
        "motherboard__manufacturer",
        "motherboard__product"
    ]
    
    list_filter = [
        "operating_system_name",
        "operating_system_architecture",
        "release",
        "machine",
        "processor",
        "motherboard__manufacturer",
        "motherboard__product",
    ]
    
    def show_memory_capacity(self, obj: System):
        return f"{obj.memory_capacity() / 1_000_000_000} GB"
    show_memory_capacity.short_description = "Memory Capacity"
    
    def show_disk_capacity(self, obj: System):
        return f"{obj.disk_capacity() / 1_000_000_000} GB"
    show_disk_capacity.short_description = "Disk Capacity"
    
    def motherboard__manufacturer(self, obj: System):
        if obj.motherboard is not None:
            return obj.motherboard.manufacturer
        return 'N/A'
    motherboard__manufacturer.short_description = _("Motherboard Manufacture")
    
    def motherboard__product(self, obj: System):
        if obj.motherboard is not None:
            return obj.motherboard.product
        return 'N/A'
    motherboard__product.short_description = _("Motherboard Product")
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('memories', 'disk_drives', 'motherboard')
