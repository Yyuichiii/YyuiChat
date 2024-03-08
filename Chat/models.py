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
