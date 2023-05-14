from django.db import models
from usuarios.models import Usuario

# Create your models here.
class PerroAdopcion(models.Model):
    class Sexo(models.TextChoices):
        M = 'MACHO'
        H = 'HEMBRA'
        NS = '-'
    
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    nombre = models.CharField(max_length=20, blank=False, null=True, default="")
    sexo = models.CharField(
        max_length = 6,
        choices=Sexo.choices,
        default=Sexo.NS
    )

    color = models.CharField(max_length=20, blank=False, null=True, default="")
    edad = models.CharField(max_length=20, blank=False, null=True, default="")
    peso = models.CharField(max_length=5, blank=False, null=True, default="")
    contacto = models.CharField(max_length=50, blank=False, null=True, default="")
    altura = models.CharField(max_length=5, blank=False, null=True, default="")
    raza = models.CharField(max_length=20, blank=False, null=True, default="")
    historial_vacunacion = models.CharField(max_length=500, blank=False, null=True, default="")
    descripcion = models.CharField(max_length=500, blank=False, null=True, default="")
    adoptado = models.BooleanField(default=False)
    publicador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="publicador_perro_adopcion")

    REQUIRED_FIELDS = ["nombre", "color", "raza", "sexo", "edad", "peso", "altura", "historial_vacunacion"]