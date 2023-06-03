from django.urls import path
from . import views

app_name = "turnos"
urlpatterns = [
    path("", views.index, name='index'),
    path("solicitar/", views.solicitar, name='solicitar'),
<<<<<<< HEAD
    path("elegir/", views.elegir_perro, name="elegir_perro")
=======
    path("asignar/<int:id>/", views.asignar, name='asignar'),
>>>>>>> dev
]