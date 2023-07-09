from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "busqueda"
urlpatterns =[
    path("publicar", views.publicar_perro, name="publicar"),
    path("mis_publicaciones", views.mis_publicaciones, name="mis_publicaciones"),
    path("index", views.listar, name="index"),
    path("info/<int:id>", views.info, name="info"),
    path("eliminar/<int:id>", views.eliminar, name="eliminar"),
    path("encontrado/<int:id>", views.marcar_encontrado, name="marcar_encontrado"),
    path("modificar/<int:id>", views.modificar, name="modificar"),
    path("filtrar/<filtro>", views.filtrar, name="filtrar_listado"),
    path("filtrar_mis_publicaciones/<filtro>", views.filtrar_mis_publicaciones, name="filtrar_mis_publicaciones")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)