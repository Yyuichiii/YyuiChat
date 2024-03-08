from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import ChatLog
import json


class MyConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("-------------1----------------")
        # Retrieve the user name from the scope
        user = self.scope["user"]
        
        # Retrieve the channel name from the scope
        channel_name = self.channel_name

        # Save the user with the channel name in the database
        await self.save_user_to_chat_log(user, channel_name)

        await self.send({
            "type": "websocket.accept",
        })
        print("-------------2----------------")
        

    async def websocket_receive(self, event):
        print("-------------3----------------")
        # Parse the received JSON-formatted message
        
        json_message = event.get("text", "")
        message_data = json.loads(json_message)

        receiver_channel=await self.Get_Channel_name(message_data['user'])
        # Get the channel layer
        channel_layer = self.channel_layer

        # Send the message asynchronously
        await channel_layer.send(receiver_channel,{
            "type": "websocket.send_to_receiver",
            "text": message_data['text'],
                })
        print("-------------4----------------")
       

    async def websocket_disconnect(self, event):
        user = self.scope["user"]
        await self.delete_user_from_chat_log(user)
        raise StopConsumer()
    

    @database_sync_to_async
    def delete_user_from_chat_log(self,user):
        chat_log=ChatLog.objects.get(user=user)
        chat_log.delete()    

    @database_sync_to_async
    def save_user_to_chat_log(self, user, channel_name):
        # Save the user with the channel name in the ChatLog model
        chat_log, created = ChatLog.objects.get_or_create(user=user)
        chat_log.channel_name = channel_name
        chat_log.save()


    @database_sync_to_async
    def Get_Channel_name(self,receiver):
        receive=ChatLog.objects.get(user=receiver)
        return receive.channel_name
    
    async def websocket_send_to_receiver(self, event):
        
        # Send message to WebSocket
        await self.send({
        'type':'websocket.send',
        'text': event['text']})