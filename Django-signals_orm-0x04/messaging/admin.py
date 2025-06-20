from django.contrib import admin
from .models import Message, Notification, MessageHistory

# Register your models here. to make them available in the admin panel
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)
