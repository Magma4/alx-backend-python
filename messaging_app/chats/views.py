from django.shortcuts import render
from rest_framework import viewsets, status
from models import Conversation, Message
from django.contrib.auth.models import User
from chats.serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipant, IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """Viewset for listing Conversation"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def get_queryset(self):
        # Filter conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        participants_info = request.data.get('participants', [])
        if len(participants_info) < 2:
            return Response({"error": "Participants should be more than 1."}, status=status.HTTP_400_BAD_REQUEST)
        
        participants = User.objects.filter(user_id__in=participants_info)

        if participants.count() != len(participants_info):
            return Response({"error": "Participants are not more than 1."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new conversation and add participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MessageViewSet(viewsets.ModelViewset):
    """Viewset for listing Message"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'conversation']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Filter messages related to conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        
        

        sender = User.objects.get(user_id=sender_id)
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        if len(message_body) > 500:
            return Response({"error": "Message cannot be more than 500 characters."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)