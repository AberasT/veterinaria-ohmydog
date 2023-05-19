from django.urls import path
from . import views

app_name = "adopcion"
urlpatterns = [
    path("", views.index, name='index'),
    path("publicar", views.publicar_perro, name="publicar"),
    path("listar", views.listar, name="listar"),
    path("info/<int:id>", views.info, name="info"),
    path("publicaciones", views.mis_publicaciones, name="mis_publicaciones"),
    path("eliminar/<int:id>", views.eliminar, name="eliminar"),
    path("adoptado/<int:id>", views.marcar_adoptado, name="marcar_adoptado")
]