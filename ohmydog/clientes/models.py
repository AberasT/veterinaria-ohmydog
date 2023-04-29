from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class Cliente(AbstractBaseUser):

    dni = models.IntegerField(unique=True)
    email = models.EmailField()
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)
    clave = models.CharField(max_length=12)

    USERNAME_FIELD = "dni"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "email", "telefono"]

    def __str__(self):
        return f"{self.dni} + {self.nombre} + {self.apellido} + {self.telefono} + {self.email} + {self.clave}"



class Perro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cliente_perros")