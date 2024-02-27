
from django.urls import path

from . import views

urlpatterns = [
    path('<str:id>/', views.chatPage, name='chat_messages'),
    path('', views.private_chat_home, name='chat_home'),
    
]
