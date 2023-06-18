from django.urls import path
from . import views

app_name = "atenciones"
urlpatterns = [
    path("agregar_vacuna/<int:id>", views.agregar_vacuna, name='agregar_vacuna'),
    path("agregar_atencion/<int:id>", views.agregar_atencion, name='agregar_atencion'),
]