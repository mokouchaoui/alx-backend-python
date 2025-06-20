from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    unread = UnreadMessagesManager() # Custom manager
    objects = models.Manager() # Default manager

    def __str__(self):
        return f"{self.content} from {self.sender} to {self.receiver} ({'Read' if self.is_read else 'Unread'})"


class Notification(models.Model):
    receiver = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
        

class MessageHistory(models.Model):
    sender = models.ForeignKey(User, related_name='sent_history', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_history', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, related_name='edited_history', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content} (edited by {self.edited_by})'