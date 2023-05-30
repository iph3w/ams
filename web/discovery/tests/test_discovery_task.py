from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings


class DiscoveryTaskTestCase(TestCase):
    def call_command(self):
        out = StringIO()

        call_command(
            "initialize",
            stdout=out,
            stderr=StringIO(),
        )
        return out.getvalue()

    def test_create_default_users(self):
        out = self.call_command()
        self.assertEqual(out, "\x1b[32;1mdefault admin user created\x1b[0m\n\x1b[32;1mdefault agent user created\x1b[0m\n")

    def test_reset_default_users_password(self):
        self.call_command()
        out = self.call_command()
        self.assertEqual(out, "\x1b[32;1mdefault admin user information reset\x1b[0m\n\x1b[32;1mdefault agent user information reset\x1b[0m\n")
