from django.forms import ModelForm
from .models import Perro
from django.forms.widgets import DateInput

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarPerroForm(ModelForm):
    class Meta:
        model = Perro
        fields = ["nombre", "raza", "color", "sexo", "fecha_nacimiento", "peso"]
        widgets = {
            'fecha_nacimiento': DateInput(attrs={'type': 'date'})
        }