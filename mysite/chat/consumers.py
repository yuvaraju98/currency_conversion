# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from .storage import store
from . import tasks


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         print("comeshere")
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         tone=tasks.get_tone(message)
#         tasks.upload_chat_task(message,tone)
#         self.send(text_data=json.dumps({
#             'message': message,
#             'sender':store.obj,
#             'tone':tone
#         }))

# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chatroom'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # pass
        #  Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        tone = tasks.get_tone(message)
        tasks.upload_chat_task(message, tone)
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': store.obj,
            'tone': tone
        }))
