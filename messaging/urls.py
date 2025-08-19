# messaging/urls.py
from django.urls import path
from .views import get_or_create_conversation, send_message, get_messages,list_conversations

urlpatterns = [
    path('conversations/<int:user_id>/', get_or_create_conversation, name='get_or_create_conversation'),
    path('messages/', send_message, name='send_message'),
    path('messages/<int:conversation_id>/', get_messages, name='get_messages'),
    path('messages/get_conversations/', list_conversations, name='get_messages'),
]
 