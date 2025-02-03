# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread messages for the specified user.
        Uses .only() to fetch only essential fields: id, sender (only its id), content, and timestamp.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender_id', 'content', 'timestamp')
