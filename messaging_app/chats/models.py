from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid

# Create your models here.
# Create User Model
class User(AbstractUser):
    ROLES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

# Create Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Create Message Model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"