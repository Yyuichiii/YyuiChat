from django.contrib import admin
from .models import ChatLog
# Register your models here.

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel_name', 'last_activity')
    search_fields = ['user__username', 'channel_name']