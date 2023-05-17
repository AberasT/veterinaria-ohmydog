from django.db import models

# Create your models here.

class Cuidador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, null=True, default="")
    edad = models.CharField(max_length=20, blank=False, null=True, default="")
    horario_inicio = models.CharField(max_length=10, blank=False, null=True, default="")
    horario_fin = models.CharField(max_length=10, blank=False, null=True, default="")
    experiencia = models.CharField(max_length=10, blank=False, null=True, default="")
    tiempo_con_veterinaria = models.CharField(max_length=10, blank=True, null=True, default="")
    contacto = models.CharField(max_length=50, blank=False, null=True, default="")

    REQUIRED_FIELDS = ["nombre", "edad", "horario_inicio", "horario_fin", "experiencia", "contacto"]
