from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    threaded_replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        # List fields you want to return; include threaded_replies
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message', 'threaded_replies']

    def get_threaded_replies(self, obj):
        # Use select_related/prefetch_related optimization if needed;
        # assume that 'replies' was already prefetched in the view.
        replies = obj.replies.all()
        serializer = MessageSerializer(replies, many=True, context=self.context)
        return serializer.data
