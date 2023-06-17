from django.db import models
from perros.models import Perro

# Create your models here.
class Turno(models.Model):
    MOTIVO_CHOICES = [
        ('vacunación antirrábica', 'Vacunación Antirrábica'),
        ('vacunación general', 'Vacunación General'),
        ('castración', 'Castración'),
        ('consulta', 'Consulta general'),
        ('desparasitación', 'Desparasitación')
    ]

    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=False, null=False)
    hora = models.TimeField(null=True)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_turnos")
    motivo = models.CharField(
        max_length=25,
        choices=MOTIVO_CHOICES, blank=True)
    detalles = models.CharField(max_length=50, null=False, blank=True, default="")
    