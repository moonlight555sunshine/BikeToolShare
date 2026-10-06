from django.urls import path
from django.views import View

from chat.views import booking_chat_room, ChatListView

app_name = 'chat'

urlpatterns = [
    path('room/<int:booking_id>/', booking_chat_room, name='booking_chat_room'),
    path('rooms/', ChatListView.as_view(), name='chat_list'),
]