import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync , sync_to_async
from channels.db import database_sync_to_async
from .models import message as msg , User 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        try:
            await self.accept()
        except Exception as e:
            print("Error in connection")
            print(e)
        self.room_group_name =  self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["user"]
        self.username = self.user.username
        print(self.username)
        #add a user to a groupe 
        await self.channel_layer.group_add(
            self.room_group_name, #groupe name
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            "sender":self.user.username
        }))

    
    async def receive(self , text_data):
        json_data = json.loads(text_data)
        message = json_data["message"]
        sender = json_data["sender"]
        print("message : "+message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message,
                "sender":sender
            }
        )
        await self.save_message(message , sender)
    
    @database_sync_to_async
    def save_message(self, message, sender):
        new_message = msg.objects.create(
            chat_room=self.room_group_name,
            sender=User.objects.get(username=sender),
            message=message
        )
        new_message.save()
    async def chat_message(self , event):
        message = event['message']
        sender = event["sender"]
        await self.send(text_data=json.dumps({
            'type':'chat',
            "message":message,
            "sender":sender
        }))