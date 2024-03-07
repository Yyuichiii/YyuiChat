from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
class MyConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("1")
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print("2")
        print(event)
        await self.send({
            "type": "websocket.send",
            "text": "Message from the server",
        })

    async def websocket_disconnect(self, event):
        print("3")
        raise StopConsumer()