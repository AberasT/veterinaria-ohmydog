from django.db import models
from usuarios.models import Usuario
# Create your models here.


class Perro(models.Model):
    class Sexo(models.TextChoices):
        macho = 'MACHO'
        hembra = 'HEMBRA'
        NS = '-'

    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, null=True, default="")
    color = models.CharField(max_length=20, blank=False, null=True, default="")
    raza = models.CharField(max_length=20, blank=True, null=True, default="")
    sexo = models.CharField(
        max_length=6,
        choices=Sexo.choices,
        default=Sexo.NS)
    fecha_nacimiento = models.DateField()
    peso = models.CharField(max_length=5, blank=True, null=True, default="")
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuarios_perros")

    REQUIRED_FIELDS = ["nombre", "color", "raza", "sexo", "fecha_nacimiento", "peso"]