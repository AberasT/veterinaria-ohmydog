from django.forms import Form, CharField, ChoiceField, ModelForm
from django import forms
from .models import Cuidador
from django.forms.widgets import TimeInput

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarCuidadorForm(ModelForm):
    class Meta:
        model = Cuidador
        fields = ["nombre_completo", "edad", "horario_inicial", "horario_final", "experiencia", "contacto"]
        widgets = {
            'horario_inicial': TimeInput(attrs={'type': 'time'}),
            'horario_final' : TimeInput(attrs={'type': 'time'})
        }