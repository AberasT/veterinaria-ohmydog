from django.urls import path
from . import views

app_name = "turnos"
urlpatterns = [
    path("", views.index, name='index'),
    path("elegir/", views.elegir_perro, name='elegir_perro'),
    path("solicitar/<int:id>/", views.solicitar, name='solicitar'),
    path("asignar/<int:id>/", views.asignar, name='asignar'),
    path("asignar_elegir/", views.asignar_elegir, name='asignar_elegir'),
    path("mis_turnos/", views.mis_turnos, name='mis_turnos'),
    path("turnos_fecha/", views.turnos_fecha, name='turnos_fecha'),
    path("confirmar_asistencia/", views.confirmar_asistencia, name='confirmar_asistencia'),
    path("turno_asistio/<int:id>/", views.turno_asistio, name='turno_asistio'),
]