from django.db import models
from usuarios.models import Usuario

# Create your models here.

class Cuidador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=20, blank=False, null=True, default="")
    edad = models.CharField(max_length=20, blank=False, null=True, default="")
    horario_inicial = models.TimeField()
    horario_final = models.TimeField()
    experiencia = models.CharField(max_length=10, blank=False, null=True, default="")
    tiempo_con_veterinaria = models.DateField(auto_now_add=True)
    contacto = models.CharField(max_length=50, blank=False, null=True, default="")

    REQUIRED_FIELDS = ["nombre_completo", "edad", "horario_inicial", "horario_final", "experiencia", "contacto"]

class Solicitud(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="solicitudes", blank=True, null=True)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name="solicitudes")
    aprobada = models.BooleanField(default=False)
    nombre = models.CharField(max_length=20, blank=True, null=True, default="")
    apellido = models.CharField(max_length=20, blank=True, null=True, default="")
    email = models.EmailField(null=True)

