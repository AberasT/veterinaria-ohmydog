from django.urls import path
from . import views

app_name = "cuidadores"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/", views.registrar, name='registrar'),
    path("eliminar/<int:id>/", views.eliminar, name='eliminar'),
    path("modificar/<int:id>/", views.modificar, name='modificar'),
    path("solicitar/<int:id>/", views.solicitar, name='solicitar'),
    path("listar_solicitudes/<int:id>/", views.listar_solicitudes, name='listar_solicitudes'),
    path("aceptar_solicitud/<int:id>/", views.aceptar_solicitud, name='aceptar_solicitud'),
    path("rechazar_solicitud/<int:id>/", views.rechazar_solicitud, name='rechazar_solicitud'),
    path("solicitar_visitante/<int:id>/", views.solicitar_visitante, name='solicitar_visitante')
]