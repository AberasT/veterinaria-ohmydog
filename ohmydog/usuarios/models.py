from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class UsuarioManager(BaseUserManager):
    
    def create_user(self, dni, email, nombre, apellido, telefono, clave, is_staff, is_superuser, **other_fields):
        email = self.normalize_email(email)
        usuario = self.model(dni=dni, email=email, nombre=nombre, apellido=apellido, telefono=telefono, clave=clave, password=clave, is_staff=is_staff, is_superuser=is_superuser)
        usuario.set_password(clave)
        usuario.save()
        return usuario
    
    def create_superuser(self, dni, email, nombre, apellido, telefono, clave, **other_fields):
        is_staff = True
        is_superuser = True

        return self.create_user(dni, email, nombre, apellido, telefono, clave, is_staff, is_superuser, **other_fields)
        
class Usuario(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True, auto_created=True, verbose_name="id")
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email address already exists.",
    })
    dni = models.IntegerField()
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)
    clave = models.CharField(max_length=12)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "dni", "telefono", "clave"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.id}, {self.email}, {self.nombre} {self.apellido}, {self.telefono}, {self.dni}, {self.clave}, is_staff: {self.is_staff}"
    