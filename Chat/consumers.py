from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import ChatLog
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("-------------1----------------")
        # Retrieve the user name from the scope
        user = self.scope["user"]
        
        # Retrieve the channel name from the scope
        channel_name = self.channel_name

        # Save the user with the channel name in the database
        await self.save_user_to_chat_log(user, channel_name)

        await self.accept()
        print("-------------2----------------")
        

    async def receive(self, text_data=None, bytes_data=None):
        print("-------------3----------------")

        # this deals with images 
        if bytes_data:
            
            await self.send(bytes_data=bytes_data)
            return
        


        message_data = json.loads(text_data)
        receiver_channel=await self.Get_Channel_name(message_data['receive_id'])
        
        # This has to work after the database thing is sorted
        if receiver_channel is None:
            data = {
             "text": "is not online"
                }
            
            # Convert the dictionary to a JSON string
            json_data = json.dumps(data)
            await self.send(text_data=json_data)
        else:
            # Get the channel layer
            channel_layer = self.channel_layer

            # Send the message asynchronously
            await channel_layer.send(receiver_channel,{
                "type": "websocket.send_to_receiver",
                "text": text_data,
            
                    })
        print("-------------4----------------")
       

    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.delete_user_from_chat_log(user)
        raise StopConsumer()
        await self.close()
    

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
        receive=ChatLog.objects.filter(user=receiver).first()
        if receive is None:
            return None
        return receive.channel_name
    
        
    
    async def websocket_send_to_receiver(self, event):
        print(event)
        # Send message to WebSocket
        await self.send(text_data=event['text'])
       