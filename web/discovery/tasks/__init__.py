from app.celery import app
from .discovery import DiscoveryTask, discovery_task


__all__ = [
    'DiscoveryTask', 'discovery_task'
]
