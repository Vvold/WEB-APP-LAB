from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

connected_users = set()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        self.username = self.scope['user'].username

        if self.scope['user'].is_authenticated:
            connected_users.add(self.username)
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        if self.scope['user'].is_authenticated:
            connected_users.discard(self.username)
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username
        }))


from channels.generic.websocket import AsyncWebsocketConsumer


class EmailLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("email_logs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("email_logs", self.channel_name)

    async def email_log_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
