from django.shortcuts import render
from rest_framework import viewsets
from models import Conversation, Message
from django.contrib.auth.models import User
from chats.serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response


# Create your views here.
class ConversationViewSet(viewsets.ViewSet):
    """Viewset for listing Conversation"""
    def list(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)
    
class MessageViewSet(viewsets.Viewset):
    """Viewset for listing Message"""
    def list(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

