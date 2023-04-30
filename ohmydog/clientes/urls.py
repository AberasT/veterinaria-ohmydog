from django.urls import path
from . import views

app_name = "clientes"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar_cliente/", views.registrar_cliente, name='registrar_cliente'),
    path("registrar_perro/<int:dni>/", views.registrar_perro, name='registrar_perro'),
    path("listar/", views.listar, name='listar'),
    path("eliminar/<int:dni>/", views.eliminar, name='eliminar'),
    path("info/<int:dni>/", views.ver_cliente, name='info')
]