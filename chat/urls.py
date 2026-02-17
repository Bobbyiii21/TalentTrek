from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat.index'),
    path('<uuid:room_id>', views.room, name='chat.room'),
    path('<uuid:room_id>/send_message', views.send_message, name='chat.send_message'),
    path('create_room/<int:participant_id>', views.create_room, name='chat.create_room'),
]