from django.urls import path
from . import views

app_name = "perros"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/<int:dni>/", views.registrar, name='registrar'),
    path("listar/", views.listar, name='listar'),
    # path("eliminar/<int:dni>/", views.eliminar, name='eliminar'),
    # path("info/<int:dni>/", views.ver_perro, name='info')
]