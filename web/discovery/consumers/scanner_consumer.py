import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ScannerProgressConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__pk = None
        self.__instance = None

    @property
    def scanner_key(self):
        from discovery.models import Scanner
        if isinstance(self.__instance, Scanner):
            return str(self.__instance.uuid)
        return self.__class__.__name__

    async def get_data(self):
        from discovery.models import Scanner
        if await Scanner.objects.filter(pk=self.__pk).aexists() is True:
            self.__instance = await Scanner.objects.aget(pk=self.__pk)
            return self.__instance.get_status()
        return {
            "status": {"progress": 0},
            "graph": {}
        }

    async def connect(self):
        self.__pk = self.scope["url_route"]["kwargs"]["pk"]
        data = await self.get_data()
        await self.channel_layer.group_add(
            self.scanner_key,
            self.channel_name,
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.scanner_key,
            {"type": "send_status", "scanner_status": data}
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.scanner_key,
            self.channel_name,
        )
        await super().disconnect(code)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.scanner_key,
            {"type": "send_status", "scanner_status": await self.get_data()}
        )

    async def send_status(self, event):
        await self.send(text_data=json.dumps({"data": event["scanner_status"]}))
