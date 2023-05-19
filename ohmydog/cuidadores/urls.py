from django.urls import path
from . import views

app_name = "cuidadores"
urlpatterns = [
    path("", views.index, name='index'),
    path("registrar/", views.registrar, name='registrar'),
    path("eliminar/<int:id>/", views.eliminar, name='eliminar')
]