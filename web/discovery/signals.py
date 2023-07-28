from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Discovery, Scanner
from .tasks import network_scanner_task, network_discovery_task


@receiver(post_save, sender=Discovery, dispatch_uid="run_discovery_task")
def run_discovery_task(sender, instance: Discovery, created, **kwargs):
    if created and instance.start_automatically is True:
        network_discovery_task.delay(
            instance=instance.pk,
            verbose=True, very_verbose=False
        )


@receiver(post_save, sender=Scanner, dispatch_uid="run_scanner_task")
def run_scanner_task(sender, instance: Scanner, created, **kwargs):
    if created and instance.start_automatically is True:
        network_scanner_task.delay(
            instance=instance.pk,
            verbose=True, very_verbose=False
        )
