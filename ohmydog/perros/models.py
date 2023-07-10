from django.db import models
from usuarios.models import Usuario
# Create your models here.


class Perro(models.Model):
    SEXO_CHOICES = [
        ("macho", "MACHO"),
        ("hembra", "HEMBRA"),
        ("ns", "NS")
    ]

    RAZA_CHOICES = [
        ("mestizo", "MESTIZO"),
        ("Siberian Husky", "SIBERIAN HUSKY"),
        ("Beagle", "BEAGLE"),
        ("Rottweiler", "ROTTWEILER"),
        ("Bull Terrier", "BULL TERRIER"),
        ("Bulldog Frances", "BULLDOG FRANCES"),
        ("Boxer", "BOXER"),
        ("Dogo Argentino", "DOGO ARGENTINO"),
        ("Gran Danes", "GRAN DANES"),
        ("Labrador", "LABRADOR"),
        ("Galgo", "GALGO"),
        ("Shiba Inu", "SHIBA INU"),
        ("Akita Inu", "AKITA INU"),
        ("Golden", "GOLDEN"),
        ("Dalmata", "DALMATA"),
        ("Chihuahua", "CHIHUAHUA"),
        ("San Bernardo", "SAN BERNARDO"),
        ("Doberman", "DOBERMAN"),
        ("Pastor Aleman", "PASTOR ALEMAN")
    ]
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, null=True, default="")
    color = models.CharField(max_length=20, blank=False, null=True, default="")
    raza = models.CharField(max_length=20, choices=RAZA_CHOICES, null=True, default="")
    sexo = models.CharField(
        max_length=6,
        choices=SEXO_CHOICES
    )
    fecha_nacimiento = models.DateField()
    peso = models.CharField(max_length=5, blank=True, null=True, default="")
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuarios_perros")
    castrado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    responsable_activo = models.BooleanField(default=True)
    REQUIRED_FIELDS = ["nombre", "color", "raza","castrado", "sexo", "fecha_nacimiento", "peso"]