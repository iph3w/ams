import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")


class AppCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super().gen_task_name(name, module)


app = AppCelery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks([a for a in settings.INSTALLED_APPS])
