from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access, send, update, or delete messages and conversations.
    """

    def has_permission(self, request, view):
        # Allow access only for authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow participants to view, send, update, and delete
        if hasattr(obj, 'participants'):
            # Check if the user is a participant of the conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Check if the user is a participant in the conversation of the message
            return request.user in obj.conversation.participants.all()
        return False