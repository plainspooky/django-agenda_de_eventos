from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localdate
from django.views.defaults import bad_request, server_error
from .models import Event
from .forms import EventForm

from datetime import datetime, timedelta


def split_date(string_date):
    """transforma a data em YYYY-MM-DD em uma tupla de três valores para
    utilizar na visão de eventos de um determinado dia."""
    for value in string_date.split('-'):
        yield int(value)


# Create your views here.
def index(request):
    context = {
        'priorities': Event.priorities_list,
        'today': localdate(),
        'hide_new_button': 'true',
    }
    return render(request, 'index.html', context)


def ops(request):
    return render(request, 'ops.html')

def all(request):
    """Exibe todas os eventos consolidados em uma única página, não recebe
    parâmetros."""
    context = {
        'events': Event.objects.order_by('-date', '-priority', 'event'),
            'priorities': Event.priorities_list,
            'today': localdate(),
    }
    return render(request, 'events.html', context)


def day(request, year: int, month: int, day: int):
    """Visualização dos eventos de um determinado dia, recebe a data em
    formato ano/mês/dia como parâmtro."""
    day = datetime(year, month, day)
    context = {
        'today': localdate(),
            'day': day,
            'events': Event.objects.filter(
                date='{:%Y-%m-%d}'.format(day)).order_by('-priority', 'event'),
            'next': day + timedelta(days=1),
            'previous': day - timedelta(days=1),
            'priorities': Event.priorities_list,
    }
    return render(request, 'day.html', context)


def delete(request, id: int):
    """Apaga um evento específico, se o evento não existir resultará em erro
    404, se algo errado ocorrer retornará a página de erro."""
    event = get_object_or_404(Event, id=id)
    (year, month, day) = tuple(
        split_date('{:%Y-%m-%d}'.format(event.date)))
    if event.delete():
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return server_errror(reqest, 'ops_500.html')


def edit(request):
    """Edita o conteúdo de um evento, recebendo os dados enviados pelo
    formulário, validando e populando em um evento já existente."""
    form = EventForm(request.POST)
    if form.is_valid():
        event = get_object_or_404(Event, id=request.POST['id'])
        event.date = form.cleaned_data['date']
        event.event = form.cleaned_data['event']
        event.priority = form.cleaned_data['priority']
        event.save()
        (year, month, day) = tuple(
            split_date('{:%Y-%m-%d}'.format(event.date)))
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return bad_request(request, None, 'ops_400.html')

# def error():

def new(request):
    """Recebe os dados de um novo evento via POST, faz a validação dos dados
    e aí insere na base de dados."""
    form = EventForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        # uso a data enviada pelo formulário para o redirecionamento.
        (year, month, day) = tuple(
            split_date(request.POST['date']))
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return bad_request(request, None, 'ops_400.html')


def show(request, id: int):
    """Visualização de um determinado evento, recebe o 'id' do evento."""
    event = get_object_or_404(Event, id=id)
    context = {
        'event': event,
            'priorities': Event.priorities_list,
            'today': localdate(),
    }
    return render(request, 'show.html', context)
