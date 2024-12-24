from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'full_name' ]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'

    def get_sender(self, Message):
        return {"username": Message.sender.username, "email": Message.sender.email}
    
    def validate_message_body(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Message cannot be more than 500 characters.")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, source='messages')
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']