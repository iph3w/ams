from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ASMAdminSite(admin.AdminSite):
    """AMSAdminSite
    """
    site_header = _("Assets Management System Administration")
    site_title = _("Assets Management System")
    index_title = _("A.M.S")
    enable_nav_sidebar = True


admin_site = ASMAdminSite(name='ams_admin')
