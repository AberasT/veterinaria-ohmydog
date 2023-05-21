from django.urls import path
from . import views

app_name = "turnos"
urlpatterns = [
    path("", views.index, name='index'),
    path("solicitar/", views.solicitar, name='solicitar'),
    path("asignar/<int:id>/", views.asignar, name='asignar'),
]