"""Inventory Admin
"""
from django.contrib import admin
from .models import System, User, Printer, DeviceType, Device
from inventory.admin_model import SystemAdmin, UserAdmin, PrinterAdmin, DeviceTypeAdmin, DeviceAdmin


admin.site.register(System, SystemAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Printer, PrinterAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Device, DeviceAdmin)
