from django.db import models
from clientes.models import Cliente
# Create your models here.


class Perro(models.Model):
    class Sexo(models.TextChoices):
        M = 'MACHO'
        H = 'HEMBRA'
        NS = '-'

    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, null=True, default="-")
    color = models.CharField(max_length=20, blank=False, null=True, default="-")
    raza = models.CharField(max_length=20, blank=True, null=True, default="-")
    sexo = models.CharField(
        max_length=6,
        choices=Sexo.choices,
        default=Sexo.NS)
    fecha_nacimiento = models.DateField()
    peso = models.CharField(max_length=5, blank=True, null=True, default="-")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cliente_perros")

    REQUIRED_FIELDS = ["nombre", "color", "raza", "sexo", "fecha_nacimiento", "peso"]