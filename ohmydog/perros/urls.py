from django.urls import path
from . import views

app_name = "perros"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/<int:id>/", views.registrar, name='registrar'),
    path("listar/", views.listar, name='listar'),
    path("eliminar/<int:id>/", views.eliminar, name='eliminar'),
    path("info/<int:id>/", views.ver_perro, name='info'),
    path("modificar/<int:id>/", views.modificar, name='modificar')
]