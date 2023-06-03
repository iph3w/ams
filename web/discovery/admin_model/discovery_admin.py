"""Device Admin
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from discovery.models import Scanner


class DiscoveryAdmin(admin.ModelAdmin):
    """Network Discovery Admin Model
    """
    list_display = [
        "ip_range",
        "created_at",
        "view_progress",
        "ended_at"
        ]

    search_fields = [
        "ip",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def ip_range(self, obj: Scanner) -> str:
        """show ip range pf the discovery task

        Args:
            obj (Scanner): _description_

        Returns:
            str: represent the ip and netmask,mask in XXX.XXX.XXX.XXX/XX format
        """
        return obj.ip_range
    ip_range.short_description = _("IP Range")

    def view_progress(self, obj: Scanner):
        """shows the progress of discovery process in percentage format

        Args:
            obj (Scanner): _description_

        Returns:
            str: represent the process progress in percentage format
        """
        return f"{obj.progress} %"

    view_progress.short_description = _("Progress")
