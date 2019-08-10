from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"comments", views.CommentViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("", views.index, name="agenda-events-index"),
    path("all", views.all, name="agenda-events-all"),
    path("<int:id>", views.show, name="agenda-events-show"),
    path("<int:year>/<int:month>/<int:day>", views.day, name="agenda-events-day"),
    path("new", views.new, name="agenda-events-new"),
    path("delete/<int:id>", views.delete, name="agenda-events-delete"),
    path("edit", views.edit, name="agenda-events-edit"),
]
