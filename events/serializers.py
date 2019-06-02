from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializador utilizado para a REST de eventos."""

    class Meta:
        model = Event
        fields = ("date", "event", "priority")
