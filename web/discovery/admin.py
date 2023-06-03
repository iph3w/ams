"""Inventory Admin
"""
from django.contrib import admin
from .models import Discovery, Scanner
from .admin_model import DiscoveryAdmin, ScannerAdmin


admin.site.register(Discovery, DiscoveryAdmin)
admin.site.register(Scanner, ScannerAdmin)
