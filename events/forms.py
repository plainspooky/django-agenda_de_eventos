from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    """Formulário utilizado para a inserção de novos eventos."""
    class Meta:
        model = Event
        fields = ['date', 'event', 'priority']
