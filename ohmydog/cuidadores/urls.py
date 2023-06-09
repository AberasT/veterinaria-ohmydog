from django.urls import path
from . import views

app_name = "cuidadores"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/", views.registrar, name='registrar'),
    path("eliminar/<int:id>/", views.eliminar, name='eliminar'),
    path("modificar/<int:id>/", views.modificar, name='modificar'),
    path("solicitar/<int:id>/", views.solicitar, name='solicitar')
]