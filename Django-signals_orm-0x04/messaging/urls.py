from django.urls import path
from .views import *

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('threaded-messages/', user_threaded_messages, name='user_threaded_messages'),
    path('inbox/unread/', unread_messages, name='unread_messages'),
]
