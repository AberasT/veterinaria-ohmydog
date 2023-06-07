from django.db import models
from perros.models import Perro

# Create your models here.
class Atencion(models.Model):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_atenciones")
    fecha = models.DateField(blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True)

class Vacuna(models.Model):
    VACUNA_CHOICES = [
        ('vacunacion antirrabica', 'Vacunación Antirrábica'),
        ('vacunacion general', 'Vacunación General')
    ]
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name="perros_vacunas")
    fecha = models.DateField(blank=False, null=False)
    vacuna = models.CharField(choices=VACUNA_CHOICES, max_length=25)
    dosis = models.CharField(max_length=30, blank=True)