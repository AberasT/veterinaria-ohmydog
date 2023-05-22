from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("cambiar_clave/", views.cambiar_clave, name='cambiar_clave'),
]