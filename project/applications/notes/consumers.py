import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ObjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def notify_object_created(self, event):
        object_data = event['object_data']
        await self.send(text_data=json.dumps({
            'message_type': 'object_created',
            'object_data': object_data,
        }))
