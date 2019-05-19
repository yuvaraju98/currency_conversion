# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from .storage import store
from . import tasks


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("comeshere")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        tasks.upload_chat_task(message)
        tone=tasks.get_tone(message)
        self.send(text_data=json.dumps({
            'message': message,
            'sender':store.obj,
            'tone':tone
        }))