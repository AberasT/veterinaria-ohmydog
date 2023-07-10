from django.db import models
from usuarios.models import Usuario

class PerroPerdido(models.Model):
    SEXO_CHOICES = [
        ("macho", "MACHO"),
        ("hembra", "HEMBRA"),
        ("ns", "NS")
    ]
    RAZA_CHOICES = [
        ("Desconocida", "NO SE SABE"),
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
        ("Shiba Inu", "AKITA INU"),
        ("Golden", "GOLDEN"),
        ("Dalmata", "DALMATA"),
        ("Chihuahua", "CHIHUAHUA"),
        ("San Bernardo", "SAN BERNARDO"),
        ("Doberman", "DOBERMAN"),
        ("Pastor Aleman", "PASTOR ALEMAN")
    ]

    ZONA_CHOICES = (
        ("Casco Urbano", "Casco Urbano"),
        ("Villa Elvira", "Villa Elvira"),
        ("Tolosa", "Tolosa"),
        ("Ringuelet", "Ringuelet"),
        ("Manuel B. Gonnet", "Manuel B. Gonnet"),
        ("José Hernández", "José Hernández"),
        ("Joaquín Gorina", "Joaquín Gorina"),
        ("Los Hornos", "Los Hornos"),
        ("San Carlos", "San Carlos"),
        ("City Bell", "City Bell"),
        ("Savoia", "Savoia"),
        ("Altos de San Lorenzo", "Altos de San Lorenzo"),
        ("Villa Elisa", "Villa Elisa"),
        ("El Peligro", "El Peligro"),
        ("Arturo Seguí", "Arturo Seguí"),
        ("Melchor Romero", "Melchor Romero"),
        ("Colonia Urquiza", "Colonia Urquiza"),
        ("Abasto", "Abasto"),
        ("Lisandro Olmos", "Lisandro Olmos"),
        ("Ángel Etcheverry", "Ángel Etcheverry"),
        ("Eduardo Arana", "Eduardo Arana")
    )
    
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    nombre = models.CharField(max_length=20, blank=True, null=True, default="")
    sexo = models.CharField(
        max_length = 6,
        choices = SEXO_CHOICES
    )

    color = models.CharField(max_length=20, blank=False, null=True, default="")
    edad = models.CharField(max_length=20, blank=True, null=True, default="")
    contacto = models.CharField(max_length=50, blank=False, null=True, default="")
    raza = models.CharField(max_length=20, choices=RAZA_CHOICES, null=True, default="")
    zona = models.CharField(max_length=20, choices=ZONA_CHOICES, default="Casco Urbano")
    direccion = models.CharField(max_length=20, blank=False)
    descripcion = models.CharField(max_length=500, blank=False, null=True, default="")
    imagen = models.ImageField(upload_to='images/')
    perdido = models.BooleanField(default=True)
    es_propio = models.BooleanField(default=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_encontrado = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    publicador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="publicador_perro_perdido")

    REQUIRED_FIELDS = ["color", "raza", "sexo", "edad", "peso", "contacto", "altura", "imagen"]
