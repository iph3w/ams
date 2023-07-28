from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from inventory.models import User


class UserAdmin(admin.ModelAdmin):
    list_select_related = ('system',)
    readonly_fields = [
        "username",
        "fullname",
        "local_account",
        "password_changeable",
        "password_requires",
        "password_expires",
        "started_datetime",
        "system"
    ]
    
    list_display = [
        "username",
        "fullname",
        "local_account",
        "password_changeable",
        "password_requires",
        "password_expires",
        "started_datetime",
        "system__node"
    ]
    
    search_fields = [
        "username",
        "fullname",
        "system__node"
    ]
    
    list_filter = [
        "local_account",
        "password_changeable",
        "password_requires",
        "password_expires",
    ]
    
    def system__node(self, obj: User):
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
