import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']

        if self.user.is_authenticated:
            participants = sorted([self.user.username, self.username])
            self.room_group_name = f"chat_{participants[0]}_{participants[1]}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Fetch messages safely
            # messages = await self.get_last_messages() old messages gets loaded by view
            messages = []

            for message in messages:
                await self.send(text_data=json.dumps({
                    'sender': message.sender.username,
                    'content': message.content,
                }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Save message and get receiver safely
        receiver = await self.get_receiver_user(self.username)
        await self.create_message(self.user, receiver, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'content': message_content,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'content': event['content'],
        }))

    # --- ORM Helpers wrapped with @database_sync_to_async ---

    @database_sync_to_async
    def get_last_messages(self):
        return list(
            Message.objects
            .select_related('sender', 'receiver')  # <--- this line is key
            .filter(
                sender__username=self.username,
                receiver__username=self.user.username
            )
            .order_by('-timestamp')[:10]
        )

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_receiver_user(self, username):
        return User.objects.get(username=username)
