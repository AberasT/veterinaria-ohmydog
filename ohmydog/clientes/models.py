from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class Cliente(AbstractBaseUser):

    dni = models.IntegerField(unique=True)
    email = models.EmailField()
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    clave = models.CharField(max_length=12)

    USERNAME_FIELD = "dni"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "email"]



class Perro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cliente_perros")