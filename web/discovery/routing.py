from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/discovery/discovery/(?P<pk>\d+)$", consumers.DiscoveryProgressConsumer.as_asgi()),
    re_path(r"ws/discovery/scanner/(?P<pk>\d+)$", consumers.ScannerProgressConsumer.as_asgi()),
]
