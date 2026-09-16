from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/<int:booking_id>/', views.booking_chat_room, name='booking_chat_room'),
]