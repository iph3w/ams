import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask
from .models import Discovery, Scanner
from .tasks import network_scanner_task, network_discovery_task


@receiver(post_save, sender=Discovery, dispatch_uid="run_discovery_task")
def run_discovery_task(sender, instance: Discovery, created, **kwargs):
    if created:
        if instance.start_automatically is True:
            network_discovery_task.delay(instance=instance.pk)
        else:
            if instance.crontab is not None:
                PeriodicTask.objects.create(
                    crontab=instance.crontab,
                    name=f'{instance.uuid}',
                    task='app.discovery.tasks.network_discovery_task',
                    kwargs=json.dumps({
                        'instance': instance.pk
                    })
                )


@receiver(post_save, sender=Scanner, dispatch_uid="run_scanner_task")
def run_scanner_task(sender, instance: Scanner, created, **kwargs):
    if created is True:
        if instance.start_automatically is True:
            network_scanner_task.delay(instance=instance.pk)
        else:
            if instance.crontab is not None:
                PeriodicTask.objects.create(
                    crontab=instance.crontab,
                    name=f'{instance.uuid}',
                    task='app.discovery.tasks.network_scanner_task',
                    kwargs=json.dumps({
                        'instance': instance.pk
                    })
                )
