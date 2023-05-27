import copy
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Discovery
from .tasks import discovery_task


@receiver(post_save, sender=Discovery, dispatch_uid="run_discovery_task")
def run_discovery_task(sender, instance: Discovery, created, **kwargs):
    if created:
        discovery_task.delay(
            instance=instance.pk,
            available_ip_address=copy.deepcopy(instance.available_ip_address),
            ports=[i for i in range(instance.min_port, instance.max_port + 1)],
            verbose=True, very_verbose=False
        )
