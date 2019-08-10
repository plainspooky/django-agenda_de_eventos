from rest_framework import serializers
from .models import Event, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Comentários de um determinado evento."""

    class Meta:
        model = Comment
        fields = ("author", "text", "avatar", "commented", "event")


class EventSerializer(serializers.ModelSerializer):
    """Serializador utilizado para a REST de eventos."""

    class Meta:
        model = Event
        fields = ("id", "date", "event", "text_priority", "number_of_comments")


class EventPlusCommentsSerializer(EventSerializer):
    """Serializador utilizado para a REST de eventos
    (versão com comentários)"""

    comment_event = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "date", "event", "text_priority", "comment_event")
