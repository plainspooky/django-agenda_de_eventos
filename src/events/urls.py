from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views


router = routers.DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="auth-login",),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="auth-logout",),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/v1/", include(router.urls)),
    path("", views.index, name="agenda-events-index"),
    path("all", views.all, name="agenda-events-all"),
    path("<int:id>", views.show, name="agenda-events-show"),
    path("<int:year>/<int:month>/<int:day>", views.day, name="agenda-events-day"),
    path("new", views.new, name="agenda-events-new"),
    path("delete/<int:id>", views.delete, name="agenda-events-delete"),
    path("edit", views.edit, name="agenda-events-edit"),
]
