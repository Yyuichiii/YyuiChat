from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
class MyConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("1")
        print(event)
        print(self.channel_layer)
        print(self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print("2",self.channel_name)
        print(event)
        await self.send({
            "type": "websocket.send",
            "text": f"Message from the server: {event['text']}",
        })

    async def websocket_disconnect(self, event):
        print("3")
        raise StopConsumer()