from django.db import models
from usuarios.models import Usuario
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
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuarios_turnos")
    perro = models.CharField(max_length=30)
    motivo = models.CharField(
        max_length=20,
        choices=MOTIVO_CHOICES)
    detalles = models.CharField(max_length=50, null=True, blank=True)
    