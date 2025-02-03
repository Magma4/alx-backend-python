from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import MessageSerializer
from .models import *


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user  # Get the logged-in user
    username = User.username  # Store username for response
    user.delete()  # Triggers post_delete signal automatically
    return Response({"message": f"User {username} deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_threaded_messages(request):
    # Retrieve top-level messages for the current user
    # (for example, messages they sent that are not replies)
    messages_qs = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    serializer = MessageSerializer(messages_qs, many=True, context={'request': request})
    return Response(serializer.data)
class MessageViewSet(viewsets.ModelViewSet):
    # Optimize queries: join sender and receiver, and prefetch replies.
    queryset = Message.objects.all().select_related('sender', 'receiver').prefetch_related('replies')
    serializer_class = MessageSerializer

    def retrieve(self, request, pk=None):
        # Retrieve a single message (e.g., a top-level message) with its replies.
        message = get_object_or_404(
            Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
            pk=pk
        )
        # Use the recursive method to fetch a threaded representation.
        threaded_replies = message.get_threaded_replies()
        data = {
            "message": MessageSerializer(message).data,
            "threaded_replies": self.serialize_threaded(threaded_replies)
        }
        return Response(data)

    def serialize_threaded(self, threaded):
        """
        Helper function to recursively serialize threaded replies.
        Assumes MessageSerializer is used to serialize each message.
        """
        serialized = []
        for entry in threaded:
            serialized.append({
                "message": MessageSerializer(entry["message"]).data,
                "replies": self.serialize_threaded(entry["replies"])
            })
        return serialized

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    """
    Retrieve unread messages for the logged-in user using the custom manager.
    """
    # Use the custom manager to filter unread messages
    unread_qs = unread_qs.only('id', 'sender_id', 'content', 'timestamp')

    serializer = MessageSerializer(unread_qs, many=True, context={'request': request})
    return Response(serializer.data)
