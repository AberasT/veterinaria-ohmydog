from django.forms import ModelForm
from .models import Usuario
from django import forms
from django.db import IntegrityError

class RegistrarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "dni", "nombre", "apellido", "telefono", "clave"]

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        usuarios = Usuario.objects.filter(email=email).exclude(id=self.id)
        if usuarios:
            raise forms.ValidationError("El email ingresado ya se encuentra registrado en el sistema.")
        return email
    
class ModificarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ["dni", "nombre", "apellido", "telefono"]