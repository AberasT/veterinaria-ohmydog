from django.urls import path
from . import views

app_name = "clientes"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/", views.registrar, name='registrar'),
    path("listar/", views.listar, name='listar'),
    path("eliminar/<int:dni>/", views.eliminar, name='eliminar')
]