from django.forms import Form, CharField, ChoiceField, ModelForm
from django import forms
from .models import Cuidador

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarCuidadorForm(ModelForm):
    class Meta:
        model = Cuidador
        fields = ["nombre", "edad", "horario_inicio", "horario_fin", "experiencia", "contacto"]