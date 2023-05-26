from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r"ws/discovery/(?P<room_name>\w+)/$", consumers.DiscoveryProgressConsumer.as_asgi()),
    re_path(r"ws/discovery/(?P<pk>\d+)$", consumers.DiscoveryProgressConsumer.as_asgi()),
]
