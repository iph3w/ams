""" Initialize Data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    """Initialize Data Command
    """
    help = 'Initializes Data'

    @staticmethod
    def _reset_user(user_info: dict, is_superuser: bool = False) -> bool:
        if User.objects.filter(username=user_info['USERNAME']).exists():
            user = User.objects.get(username=user_info['USERNAME'])
            user.first_name = user_info['FIRST_NAME']
            user.last_name = user_info['LAST_NAME']
            user.email = user_info['EMAIL']
            user.set_password(user_info['PASSWORD'])
            user.is_active = True
            user.is_superuser = is_superuser
            user.save()
            return True
        return False

    def handle(self, *args, **options):
        if Command._reset_user(user_info=settings.DEFAULT_ADMIN_INFO, is_superuser=True) is True:
            self.stdout.write(self.style.SUCCESS("default admin user information reset"))
        else:
            default_admin_user = User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN_INFO['USERNAME'],
                email=settings.DEFAULT_ADMIN_INFO['EMAIL'],
                password=settings.DEFAULT_ADMIN_INFO['PASSWORD'],
                first_name=settings.DEFAULT_ADMIN_INFO['FIRST_NAME'],
                last_name=settings.DEFAULT_ADMIN_INFO['LAST_NAME'],
            )
            default_admin_user.save()
            self.stdout.write(self.style.SUCCESS("default admin user created"))
        
        if Command._reset_user(user_info=settings.DEFAULT_AGENT_INFO, is_superuser=False) is True:
            self.stdout.write(self.style.SUCCESS("default agent user information reset"))
        else:
            agent_user = User.objects.create_user(
                username=settings.DEFAULT_AGENT_INFO['USERNAME'],
                email=settings.DEFAULT_AGENT_INFO['EMAIL'],
                password=settings.DEFAULT_AGENT_INFO['PASSWORD'],
                first_name=settings.DEFAULT_AGENT_INFO['FIRST_NAME'],
                last_name=settings.DEFAULT_AGENT_INFO['LAST_NAME'],
            )
            agent_user.is_active = True
            agent_user.save()
            self.stdout.write(self.style.SUCCESS("default agent user created"))
