from django.db import models
from perros.models import Perro

# Create your models here.
class Turno(models.Model):
    MOTIVO_CHOICES = [
        ('vacunacion', 'Vacunación'),
        ('castracion', 'Castración'),
        ('consulta', 'Consulta general'),
        ('urgencia', 'Consulta de urgencia'),
        ('desparasitacion', 'Desparasitación')
    ]

    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=False, null=False)
    hora = models.TimeField(null=True, blank=True)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_turnos")
    motivo = models.CharField(
        max_length=20,
        choices=MOTIVO_CHOICES)
    detalles = models.CharField(max_length=50, null=False, blank=True)
    