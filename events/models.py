from django.db import models
from django.utils import timezone
from libgravatar import Gravatar

# Create your models here.
class Event(models.Model):
    """Classe contendo o evento propriamente dito, sua data, descrição
    e também prioridade."""

    priorities_list = (
        ('0', 'Sem prioridade'),
        ('1', 'Normal'),
        ('2', 'Urgente'),
        ('3', 'Muito Urgente'),
    )

    date = models.DateField()
    event = models.CharField(max_length=80)
    priority = models.CharField(max_length=1, choices=priorities_list)

    class Meta:
        ordering = ('-date', '-priority', 'event',)
        
    def number_of_comments(self):
        """Retorna a quantidade de comentários dentro de um evento."""
        return self.comment_event.count()

    def __str__(self):
        return self.event


class Comment(models.Model):
    """Comentários efetuados em um determinado evento."""

    author = models.CharField(max_length=80)
    email = models.EmailField()
    text = models.CharField(max_length=160)
    commented = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comment_event')

    def avatar(self):
        """Retorna a partir do endereço de e-mail, um avatar
        configurado no Gravatar ou um dos avatares padrão deles."""
        g = Gravatar(self.email)
        return g.get_image(default='identicon')

    def __str__(self):
        return "{} commentou em {:%c}".format(self.author, self.commented)
