from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user  # Get the logged-in user
    username = user.username  # Store username for response
    user.delete()  # Triggers post_delete signal automatically
    return Response({"message": f"User {username} deleted successfully"}, status=status.HTTP_200_OK)
