from django.urls import path
from . import views

app_name = "atenciones"
urlpatterns = [
    path("agregar_vacuna/<int:id>", views.agregar_vacuna, name='agregar_vacuna'),
    path("agregar_atencion/<int:id>", views.agregar_atencion, name='agregar_atencion'),
    path("modificar_atencion/<int:id>", views.modificar_atencion, name='modificar_atencion'),
    path("modificar_vacuna/<int:id>", views.modificar_vacuna, name='modificar_vacuna'),
    path("eliminar_atencion/<int:id>", views.eliminar_atencion, name='eliminar_atencion'),
    path("eliminar_vacuna/<int:id>", views.eliminar_vacuna, name='eliminar_vacuna'),
]