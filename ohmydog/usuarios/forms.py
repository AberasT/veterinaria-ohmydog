from django.forms import ModelForm
from .models import Usuario

class RegistrarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "dni", "nombre", "apellido", "telefono"]