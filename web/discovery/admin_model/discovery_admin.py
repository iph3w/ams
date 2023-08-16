"""Device Admin
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from discovery.models import Discovery


class DiscoveryAdmin(admin.ModelAdmin):
    """Network Discovery Admin Model
    """
    list_display = [
        "ip_range",
        "start_automatically",
        "created_at",
        "view_progress",
        "ended_at"
    ]

    search_fields = [
        "ip", "start_automatically"
    ]

    fieldsets = (
        (None, {
            'fields': ("ip_address", "netmask", "start_automatically", "crontab")
        }),
        ('Details', {
            'fields': ("created_at", "ended_at")
        }),
    )
    readonly_fields = ("created_at", "ended_at", "progress")

    def get_queryset(self, request):
        q = super(DiscoveryAdmin, self).get_queryset(request)
        if request.user.is_superuser is True:
            return q
        return q.filter(
            start_automatically=True,
            created_by_id=request.user.pk
        )

    def has_change_permission(self, request, obj: Discovery = None):
        return False

    def has_delete_permission(self, request, obj: Discovery = None):
        if request.user.is_superuser is True:
            if obj is not None:
                if obj.start_automatically is True:
                    return True
                else:
                    if obj.created_by_id == request.user.pk:
                        return True
        else:
            if obj is not None and \
                    obj.start_automatically is True and \
                    obj.created_by_id == request.user.pk and \
                    obj.created_at <= datetime.now() + relativedelta(months=6):
                return True
        return False

    def ip_range(self, obj: Discovery) -> str:
        """show ip range pf the discovery task

        Args:
            obj (Discovery): _description_

        Returns:
            str: represent the ip and netmask,mask in XXX.XXX.XXX.XXX/XX format
        """
        return obj.ip_range

    ip_range.short_description = _("IP Range")

    def view_progress(self, obj: Discovery):
        """shows the progress of discovery process in percentage format

        Args:
            obj (Discovery): _description_

        Returns:
            str: represent the process progress in percentage format
        """
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            f'{obj.progress:.2f}'
        )

    view_progress.short_description = _("Progress")
