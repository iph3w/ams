from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings


class InitializeCommandTestCase(TestCase):
    def call_command(self):
        call_command("initialize")

    def make_sure_user_information_will_work_fine(self, user_info) -> bool:
        if User.objects.filter(username=user_info['USERNAME']).exists() is False:
            return False
        return User.objects.get(username=user_info['USERNAME']).check_password(user_info['PASSWORD'])

    def set_user_password_something_else(self, user_info, new_password):
        user = User.objects.get(username=user_info['USERNAME'])
        user.set_password(new_password)
        user.save()

    def test_create_default_users(self):
        self.call_command()
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_ADMIN_INFO))
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_AGENT_INFO))

    def test_reset_default_users_password(self):
        self.call_command()
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_ADMIN_INFO))
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_AGENT_INFO))

        # Change Password
        new_password = "NEW_PASSWORD"
        self.set_user_password_something_else(settings.DEFAULT_ADMIN_INFO, new_password)
        self.set_user_password_something_else(settings.DEFAULT_AGENT_INFO, new_password)

        # Check if passwords are changed
        self.assertTrue(
            User.objects.get(username=settings.DEFAULT_ADMIN_INFO['USERNAME']).check_password(new_password)
        )
        self.assertTrue(
            User.objects.get(username=settings.DEFAULT_AGENT_INFO['USERNAME']).check_password(new_password)
        )

        # Try to reset passwords
        self.call_command()
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_ADMIN_INFO))
        self.assertTrue(self.make_sure_user_information_will_work_fine(settings.DEFAULT_AGENT_INFO))
