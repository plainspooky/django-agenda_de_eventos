from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localdate
from django.views.defaults import bad_request, server_error
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Event, Comment
from .forms import EventForm, CommentForm
from .serializers import CommentSerializer, EventSerializer

from .services import split_date


ITEMS_PER_PAGE = 5
FIRST_PAGE = 1

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """
    Disponibiliza os eventos da agenda como uma API REST.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Disponibiliza os eventos da agenda como uma API REST.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("event__id",)

    permission_classes = (IsAuthenticated,)


@login_required
def index(request):
    """
    Exibe a página principal da aplicaão.
    """
    context = {
        "hide_new_button": True,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "index.html", context)


@login_required
def all(request):
    """
    Exibe todas os eventos consolidados em uma única página, recebe o
    número da página a ser visualizada via GET.
    """

    page = request.GET.get("page", FIRST_PAGE)
    paginator = Paginator(Event.objects.all(), ITEMS_PER_PAGE)
    total = paginator.count

    try:
        events = paginator.page(page)
    except InvalidPage:
        events = paginator.page(FIRST_PAGE)

    context = {
        "events": events,
        "total": total,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "events.html", context)


@login_required
def day(request, year: int, month: int, day: int):
    """
    Visualização dos eventos de um determinado dia, recebe a data em
    formato ano/mês/dia como parâmtro.
    """
    day = datetime(year, month, day)
    filted_events = Event.objects.filter(
        date="{:%Y-%m-%d}".format(day)
    ).order_by("-priority", "event")

    context = {
        "today": localdate(),
        "day": day,
        "events": filted_events,
        "next": day + timedelta(days=1),
        "previous": day - timedelta(days=1),
        "priorities": Event.priorities_list,
    }

    return render(request, "day.html", context)


@login_required
def delete(request, id: int):
    """
    Apaga um evento específico, se o evento não existir resultará em
    erro 404, se algo errado ocorrer retornará a página de erro.
    """
    event = get_object_or_404(Event, id=id)
    (year, month, day) = split_date("{:%Y-%m-%d}".format(event.date))

    if event.delete():
        return redirect("agenda-events-day", year=year, month=month, day=day)
    else:
        return server_errror(reqest, "ops_500.html")


@login_required
def edit(request):
    """
    Edita o conteúdo de um evento, recebendo os dados enviados pelo
    formulário, validando e populando em um evento já existente.
    """
    form = EventForm(request.POST)

    if form.is_valid():
        event = get_object_or_404(Event, id=request.POST["id"])
        event.date = form.cleaned_data["date"]
        event.event = form.cleaned_data["event"]
        event.priority = form.cleaned_data["priority"]
        event.save()
        (year, month, day) = split_date("{:%Y-%m-%d}".format(event.date))
        return redirect("agenda-events-day", year=year, month=month, day=day)
    else:
        return bad_request(request, None, "ops_400.html")


@login_required
def new(request):
    """
    Recebe os dados de um novo evento via POST, faz a validação dos dados
    e aí insere na base de dados.
    """
    form = EventForm(request.POST)

    if form.is_valid():
        form.save(commit=True)
        # uso a data enviada pelo formulário para o redirecionamento.
        (year, month, day) = split_date(request.POST["date"])
        return redirect("agenda-events-day", year=year, month=month, day=day)
    else:
        return bad_request(request, None, "ops_400.html")


def show(request, id: int):
    """
    Visualização de um determinado evento e de seus comentários, recebe
    o 'id' do evento. Caso seja acessado via POST insere um novo comentário.
    """
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("agenda-events-show", id=id)

    context = {
        "event": event,
        "comments": Comment.objects.filter(event=id).order_by("-commented"),
        "hide_new_button": True,
        "priorities": Event.priorities_list,
        "today": localdate(),
    }

    return render(request, "show.html", context)
