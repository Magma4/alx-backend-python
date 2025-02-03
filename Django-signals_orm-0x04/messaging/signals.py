from django.db.models.signals import post_save
from django.dispatch import receiver
from models import *

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create a notification for new messages
        Notification.objects.create(user=instance.receiver, message=instance)
