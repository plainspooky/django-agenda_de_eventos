from django.shortcuts import render
from django.utils.timezone import localdate, now
from .models import Event

from datetime import datetime, timedelta

# Create your views here.
def index(request):
    """Exibe todas os eventos consolidados em uma única página, não recebe
    parâmetros."""
    context = {            
           # 'today': "{:%Y/%m/%d}".format(localdate()),
            'events': Event.objects.order_by('-date', '-priority', 'event'),
            }
    return render(request, 'events.html', context)

def show(request, id):
    """Visualização de um determinado evento, recebe o 'id' do evento."""
    context = {
            'event': Event.objects.get(id=id),
            }
    return render(request, 'show.html', context)

def day(request, year, month, day):
    """Visualização dos eventos de um determinado dia, recebe a data em
    formato ano/mês/dia como parâmtro."""
    # 
    day = datetime(year, month, day)
    context = {
            'today': localdate(),
            'day':  day,
            'previous': day - timedelta(days=1),
            'next': day + timedelta(days=1),
            'events': Event.objects.filter(
                        date="{:%Y-%m-%d}".format(day)).order_by('-priority', 'event')
    }
    return render(request, 'day.html', context)

