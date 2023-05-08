from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class ClienteManager(BaseUserManager):
    
    def create_user(self, dni, email, nombre, apellido, telefono, clave, is_staff, is_superuser, **other_fields):
        email = self.normalize_email(email)
        cliente = self.model(dni=dni, email=email, nombre=nombre, apellido=apellido, telefono=telefono, clave=clave, password=clave, is_staff=is_staff, is_superuser=is_superuser)
        cliente.set_password(clave)
        cliente.save()
        return cliente
    
    def create_superuser(self, dni, email, nombre, apellido, telefono, clave, **other_fields):
        is_staff = True
        is_superuser = True

        return self.create_user(dni, email, nombre, apellido, telefono, clave, is_staff, is_superuser, **other_fields)
        
class Cliente(AbstractBaseUser, PermissionsMixin):

    dni = models.IntegerField(unique=True)
    email = models.EmailField()
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)
    clave = models.CharField(max_length=12)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "dni"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "email", "telefono", "clave"]

    objects = ClienteManager()

    def __str__(self):
        return f"{self.dni} + {self.nombre} + {self.apellido} + {self.telefono} + {self.email} + {self.clave}"
