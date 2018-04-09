from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='agenda-events-all'),
    path('<int:id>', views.show, name='agenda-events-show'),
    path('<int:year>/<int:month>/<int:day>', views.day, name='agenda-events-day'),
    ]
