from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from inventory.models import Printer


class PrinterAdmin(admin.ModelAdmin):
    list_select_related = ('system',)
    readonly_fields = [
        "caption",
        "is_network",
        "is_local",
        "port_name",
        "is_published",
        "is_shared",
        "shared_name",
        "driver_name",
        "device_id",
        "is_active",
        "system"
    ]

    list_display = [
        "caption",
        "is_network",
        "is_local",
        "port_name",
        "is_published",
        "is_shared",
        "shared_name",
        "system__node"
    ]

    search_fields = [
        "caption",
        "port_name",
        "shared_name",
        "driver_name",
        "device_id",
        "system__node"
    ]

    list_filter = [
        "is_network",
        "is_local",
        "port_name",
        "is_published",
        "is_shared",
    ]

    def system__node(self, obj: Printer):
        if obj.system is not None:
            return obj.system.node
        return 'N/A'
    system__node.short_description = _("System Node")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active=True)
