from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(receiver=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    if instance.pk:
        MessageHistory.objects.create(sender=instance.sender, receiver=instance.receiver, content=instance.content, edited_by=instance.sender)

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(sender=instance).delete()
    MessageHistory.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()