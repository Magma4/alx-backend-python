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
                    previous_content=original.content,
                    edited_by=instance.edited_by
                )
                instance.edited = True  # Mark the message as edited
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_related_data(sender, instance, **kwargs):
    """
    Deletes all messages, notifications, and message history when a user is deleted.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    Notification.objects.filter(user=instance).delete()

    print(f"Cleaned up messages, message history, and notifications for deleted user {instance.username}")
