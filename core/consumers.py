import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Function to send a message to the global broadcast group
def send_global_message(message):
    """
    Funcion para Enviar un mensaje en tiempo real
    """
    note = {}
    note['type'] = "note.message"
    note['message'] = message['note']
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("global_notes", note)


def send_notifications(message):
    """
    Funcion para Mostrar notificacion de accion en tiempo real
    """
    channel_layer = get_channel_layer()
    notification = {}
    notification['type'] = "notification.message"
    notification['message'] = message['notifications'][0]
    async_to_sync(channel_layer.group_send)("global_notification", notification)


class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to a global broadcast group
        self.room_group_name = "global_notes"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the global broadcast group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to the global broadcast group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "note.message", "message": message}
        )

    async def note_message(self, event):
        message = event["message"]

        # Send the message to the client
        await self.send(text_data=json.dumps({"message": message}))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to a global broadcast group
        self.room_group_name = "global_notification"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the global broadcast group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to the global broadcast group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "notification.message", "message": message}
        )

    async def notification_message(self, event):
        message = event["message"]

        # Send the message to the client
        await self.send(text_data=json.dumps({"message": message}))