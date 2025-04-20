import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For regular HTTP requests
    "websocket": AuthMiddlewareStack(  # For WebSocket connections
        URLRouter([
            path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),  # WebSocket route
        ])
    ),
})
