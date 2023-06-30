from django.urls import path
from . import views

app_name = "usuarios"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar-cliente/", views.registrar_cliente, name='registrar_cliente'),
    path("registrar-veterinario/", views.registrar_veterinario, name='registrar_veterinario'),
    path("modificar-cliente/<int:id>", views.modificar_cliente, name="modificar_cliente"),
    path("eliminar/<int:id>/", views.eliminar, name='eliminar'),
    path("info/<int:id>/", views.ver_cliente, name='info'),
    path("historial-clientes/", views.historial_clientes, name='historial_clientes'),
    path("recuperar-cliente/<int:id>/", views.recuperar_cliente, name='recuperar_cliente')
]