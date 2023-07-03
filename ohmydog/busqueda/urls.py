from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "busqueda"
urlpatterns =[
    path("publicar", views.publicar_perro, name="publicar"),
    path("mis_publicaciones", views.mis_publicaciones, name="mis_publicaciones"),
    path("index", views.listar, name="index")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)