from django.contrib import admin
from .models import Event, Comment

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Cria a classe EventAdmin com os parâmetros de exibição das
    informações do modelo Event dentro da interface de administração."""
    list_display = ("date", "event", "priority", )
    list_display_links = ("event", )
    list_filter = ("date", "priority", )
    list_editable = ("priority", )
    search_fields = ("event", "date", )

admin.site.register(Comment)
