from django.db import models
import uuid
from accounts.models import TTUser
# Create your models here.
class ChatUser(models.Model):
    TTUser = models.ForeignKey(TTUser, on_delete=models.CASCADE)
    last_read_message_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.user.email

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='owner')
    participant = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='participant')
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} - {self.created_at}"

    
    