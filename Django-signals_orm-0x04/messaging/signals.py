from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from models import *

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create a notification for new messages
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Ensure the message already exists (i.e., it's being updated)
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:  # Check if content changed
                MessageHistory.objects.create(
                    message=original,
                    previous_content=original.content
                )
                instance.edited = True  # Mark the message as edited
        except Message.DoesNotExist:
            pass
