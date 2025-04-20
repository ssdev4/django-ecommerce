import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']

        # Check if the user is authenticated
        if self.user.is_authenticated:
            self.room_group_name = f"chat_{self.user.username}_{self.username}"

            # Join the room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept the WebSocket connection
            await self.accept()

            # Send the last 10 messages to the user (optional)
            messages = Message.objects.filter(
                sender__username=self.username,
                receiver__username=self.user.username
            ).order_by('-timestamp')[:10]
            for message in messages:
                await self.send(text_data=json.dumps({
                    'sender': message.sender.username,
                    'content': message.content,
                }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Save message to the database
        message = Message.objects.create(
            sender=self.user,
            receiver=User.objects.get(username=self.username),
            content=message_content
        )

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'content': message_content,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'content': event['content'],
        }))
