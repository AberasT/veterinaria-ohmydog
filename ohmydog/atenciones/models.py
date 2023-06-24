from django.db import models
from perros.models import Perro

# Create your models here.
class Atencion(models.Model):
    MOTIVO_CHOICES = [
        ('vacunación antirrábica', 'Vacunación Antirrábica'),
        ('vacunación general', 'Vacunación General'),
        ('castración', 'Castración'),
        ('consulta', 'Consulta general'),
        ('desparasitación', 'Desparasitación')
    ]
    id = models.AutoField(primary_key=True)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_atenciones")
    fecha = models.DateField(blank=False, null=False)
    motivo = models.CharField(
        max_length=25,
        choices=MOTIVO_CHOICES, blank=False)
    descripcion = models.CharField(max_length=200, blank=True)

class Vacuna(models.Model):
    VACUNA_CHOICES = [
        ('vacunacion antirrabica', 'Vacunación Antirrábica'),
        ('vacunacion general', 'Vacunación General')
    ]

    id = models.AutoField(primary_key=True)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_vacunas")
    fecha = models.DateField(blank=False, null=False)
    vacuna = models.CharField(choices=VACUNA_CHOICES, max_length=25)
    dosis = models.CharField(max_length=30, blank=True)