from chat import consumers
from django.urls import re_path, path
from chat.consumers import CustomerChatConsumer


websocket_urlpatterns = [    
    path('ws/<int:id>/', CustomerChatConsumer.as_asgi())
]
