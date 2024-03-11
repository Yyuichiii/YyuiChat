from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    channel_name = models.CharField(max_length=250, blank=False)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chat Log"
        verbose_name_plural = "Chat Logs"

    def __str__(self):
        return f"{self.user.username}'s Chat Log"
    
class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        participants_list = ', '.join(str(participant) for participant in self.participants.all())
        return f"Chat between: {participants_list}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} in {self.chat}"
