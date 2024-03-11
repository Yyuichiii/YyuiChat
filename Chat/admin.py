from django.contrib import admin
from .models import ChatLog,Chat,Message
# Register your models here.

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel_name', 'last_activity')
    search_fields = ['user__username', 'channel_name']


class MessageInline(admin.TabularInline):
    model = Message
    ordering = ['-timestamp']  # Ordering messages by timestamp in descending order

class ChatAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    filter_horizontal = ('participants',)

admin.site.register(Chat, ChatAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'chat', 'timestamp', 'is_read')
    list_filter = ('chat', 'sender', 'is_read')
    search_fields = ('content',)
    readonly_fields = ('timestamp',)

admin.site.register(Message, MessageAdmin)