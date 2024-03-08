import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from Chat.consumers import MyConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YyuiChat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
     "websocket":
         AuthMiddlewareStack(
             URLRouter([
                path("chat/", MyConsumer.as_asgi()),
                
            ])
         )
        
    
})
