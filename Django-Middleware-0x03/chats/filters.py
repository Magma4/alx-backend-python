import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by sender, conversation, or a time range.
    """
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr="iexact")
    conversation = django_filters.UUIDFilter(field_name="conversation__conversation_id")

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']
