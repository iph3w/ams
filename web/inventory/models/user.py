from email.policy import default
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from .system import System


class User(models.Model):
    username = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Username"))
    fullname = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name=_("Fullname"))
    local_account = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Local Account"))
    password_changeable = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Password Changaeble"))
    password_requires = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Password Requires"))
    password_expires = models.BooleanField(default=None, null=True, blank=True, verbose_name=_("Password Expires"))
    started_datetime = models.DateTimeField(default=None, null=True, blank=True, verbose_name=_("Started Datetime"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="users")

    def __str__(self) -> str:
        return f'{self.username} [{self.fullname}] - {self.started_datetime}'
