from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for the specified user, retrieving only the essential fields.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    read = models.BooleanField(default=False)  # Indicates whether the message has been read

    # Default manager and custom unread messages manager
    objects = models.Manager()
    unread = UnreadMessagesManager()

    # Field for threaded conversations (null for top-level messages)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_threaded_replies(self):
        """
        Recursively returns a nested list of replies.
        This method uses the already prefetched 'replies' if available.
        """
        threaded = []
        for reply in self.replies.all():
            threaded.append({
                "message": reply,
                "replies": reply.get_threaded_replies()  # Recursive call
            })
        return threaded

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message from {self.message.sender}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    previous_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="edited_messages")  # Track who edited the message


    def __str__(self):
        return f"History of message {self.message.id} - Edited at {self.edited_at}"
