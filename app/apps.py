"""Assets Management System App
"""
from django.contrib.admin.apps import AdminConfig


class AMSAdminConfig(AdminConfig):
    """AMSAdminConfig
    """
    default_site = "app.admin.AMSAdminSite"
