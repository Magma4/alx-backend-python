from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Use a SerializerMethodField to include nested replies.
    threaded_replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message', 'threaded_replies']

    def get_threaded_replies(self, obj):
        # Recursively serialize the threaded replies.
        replies = obj.get_threaded_replies()
        return self.serialize_threaded(replies)

    def serialize_threaded(self, threaded):
        serialized = []
        for entry in threaded:
            serialized.append({
                "message": MessageSerializer(entry["message"], context=self.context).data,
                "replies": self.serialize_threaded(entry["replies"])
            })
        return serialized
